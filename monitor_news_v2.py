import os, time, json, re, argparse, hashlib, logging
from datetime import datetime, timezone, timedelta
from email.message import EmailMessage
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import feedparser
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# --- Load env
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# --- Storage for de-dup
SEEN_PATH = os.path.join(os.path.dirname(__file__), "seen.json")
def load_seen():
    if os.path.exists(SEEN_PATH):
        try:
            with open(SEEN_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning("Failed to load seen.json: %s", e)
            return {}
    return {}

def save_seen(seen):
    try:
        with open(SEEN_PATH, "w", encoding="utf-8") as f:
            json.dump(seen, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error("Failed to save seen.json: %s", e)

seen = load_seen()

# --- Sources (you can edit/extend)
SECP_PRESS_URL = "https://www.secp.gov.pk/media-center/press-releases/"
SOURCE_FEEDS = [
    "https://www.dawn.com/business/rss.xml",
    "https://www.thenews.com.pk/rss/1/1",          # Top Stories RSS
    "https://propakistani.pk/category/business/feed/",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (AlertsBot; +https://example.com)"
}

# --- HTTP session with retries
def make_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=frozenset(['GET', 'POST']))
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update(HEADERS)
    return session

session = make_session()

def hash_id(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def fetch_secp_press(session):
    """Scrape SECP press releases page and return list of dicts: [{'title','link','summary','id'}]"""
    items = []
    try:
        r = session.get(SECP_PRESS_URL, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # Try to find anchor tags that look like press release links
        for a in soup.select("a"):
            href = a.get("href", "")
            text = (a.get_text() or "").strip()
            if not href or not text:
                continue
            if "press" in href or "media-center" in href:
                if href.startswith("/"):
                    link = "https://www.secp.gov.pk" + href
                else:
                    link = href
                key = hash_id(text + "|" + link)
                items.append({"title": text, "link": link, "summary": "", "id": key})
        # Unique by id
        uniq = {it["id"]: it for it in items}
        return list(uniq.values())
    except Exception as e:
        logger.warning("SECP fetch failed: %s", e)
        return []

def _clean_html_summary(html):
    if not html:
        return ""
    return BeautifulSoup(html, "html.parser").get_text(separator=" ", strip=True)

def fetch_rss(session, url):
    out = []
    try:
        feed = feedparser.parse(url)
        for e in feed.entries[:20]:
            title = (e.get("title") or "").strip()
            link = (e.get("link") or "").strip()
            summary = _clean_html_summary(e.get("summary", "") or e.get("description", ""))
            key = hash_id(title + "|" + link)
            out.append({"title": title, "link": link, "summary": summary, "id": key})
    except Exception as e:
        logger.warning("RSS failed %s: %s", url, e)
    return out

def collect_items(parallel=True):
    items = []
    items.extend(fetch_secp_press(session))

    if parallel:
        with ThreadPoolExecutor(max_workers=min(8, max(2, len(SOURCE_FEEDS)))) as ex:
            futures = {ex.submit(fetch_rss, session, f): f for f in SOURCE_FEEDS}
            for fut in as_completed(futures):
                try:
                    items.extend(fut.result())
                except Exception as e:
                    logger.warning("Error fetching feed %s: %s", futures[fut], e)
    else:
        for f in SOURCE_FEEDS:
            items.extend(fetch_rss(session, f))

    # De-dup by id
    uniq = {it["id"]: it for it in items}
    return list(uniq.values())

# --- AI Summarizer (Roman Urdu)
def ai_summarize_roman(text, title, timeout_secs=10):
    prompt = f"""
Summarize the following news for a Pakistani audience in 2 short lines in Roman Urdu, very simple and casual.
Keep only the key fact (who/what) + action (ban/warning/job/report) + when (if present) + what to do (avoid/join/apply).
Return max ~35 words total.

Title: {title}
Text: {text}
"""
    # OpenAI
    if OPENAI_API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}],
                temperature=0.2,
                max_tokens=120,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            logger.warning("OpenAI failed: %s", e)

    # Groq (Llama 3.1)
    if GROQ_API_KEY:
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            resp = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role":"user","content":prompt}],
                temperature=0.2,
                max_tokens=120,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            logger.warning("Groq failed: %s", e)

    # Fallback: simple heuristic shortener + manual romanization-lite
    text = re.sub(r"\s+", " ", text or "")
    text = text[:300]
    baselines = [
        "update aayi hai",
        "important khabar hai",
        "zaroor check karein",
        "details link me",
    ]
    return f"{title[:60]} — ye important update hai, details link me dekh lo. {baselines[0]}"

# --- Email
def send_email(subject, body_text, body_html=None, dry_run=False):
    import smtplib, ssl
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD or not TO_EMAIL:
        logger.error("EMAIL env not set. Skipping email.")
        return False
    if dry_run:
        logger.info("[dry-run] Would send email: %s", subject)
        return True

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.set_content(body_text)
    if body_html:
        msg.add_alternative(body_html, subtype="html")

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        logger.error("Failed to send email: %s", e)
        return False

def format_email(item, roman_summary):
    time_str = datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')
    text_lines = [
        f"Title: {item['title']}",
        "",
        "Roman Urdu Summary:",
        roman_summary,
        "",
        f"Source: {item['link']}",
        f"Time: {time_str}",
    ]
    text = "\n".join(text_lines)

    html = f"""
    <html>
      <body>
        <h3>{item['title']}</h3>
        <p><strong>Roman Urdu Summary:</strong><br/>{roman_summary}</p>
        <p>Source: <a href="{item['link']}">{item['link']}</a></p>
        <p><small>Time: {time_str}</small></p>
      </body>
    </html>
    """
    return text, html

def prune_seen(seen_dict, max_age_days=60):
    cutoff = time.time() - max_age_days * 86400
    keys = list(seen_dict.keys())
    removed = 0
    for k in keys:
        try:
            if seen_dict.get(k, {}).get("ts", 0) < cutoff:
                del seen_dict[k]
                removed += 1
        except Exception:
            del seen_dict[k]
            removed += 1
    if removed:
        logger.info("Pruned %d old seen entries", removed)
    return removed

def process_once(limit=None, dry_run=False, prune_days=60):
    global seen
    items = collect_items(parallel=True)
    sent = 0
    processed = 0

    # simple sort: could be improved with published date
    items = sorted(items, key=lambda x: x.get("title",""))  # deterministic order
    for it in items:
        if limit and processed >= limit:
            break
        processed += 1

        if it["id"] in seen:
            continue

        text_for_ai = it["summary"] or it["title"]
        roman = ai_summarize_roman(text_for_ai, it["title"])
        text_body, html_body = format_email(it, roman)
        subj = f"[Alert] {it['title'][:70]}"
        ok = send_email(subj, text_body, body_html=html_body, dry_run=dry_run)
        if ok:
            if not dry_run:
                seen[it["id"]] = {"ts": time.time(), "title": it["title"]}
            sent += 1
            logger.info("[sent] %s", it["title"])
        else:
            logger.info("[skip] email not sent for %s", it["title"])

    if not dry_run and sent:
        save_seen(seen)

    # prune old entries optionally
    if prune_days:
        pruned = prune_seen(seen, max_age_days=prune_days)
        if pruned and not dry_run:
            save_seen(seen)

    return sent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="Run one scan and exit")
    ap.add_argument("--watch", action="store_true", help="Run in a loop (interval from env)")
    ap.add_argument("--dry-run", action="store_true", help="Do everything except actually send emails")
    ap.add_argument("--limit", type=int, default=0, help="Limit number of items processed this run (0=unlimited)")
    ap.add_argument("--test-email", action="store_true", help="Send a single test email (uses --dry-run to skip actual send if desired)")
    ap.add_argument("--prune-days", type=int, default=60, help="Prune seen entries older than this many days (0=disabled)")
    args = ap.parse_args()

    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD or not TO_EMAIL:
        logger.warning("EMAIL_* env not fully configured. Use --dry-run for testing or set EMAIL env vars to enable sending.")

    if args.test_email:
        subj = "[Test] AlertsBot test email"
        body = "This is a test from AlertsBot. If you see this, SMTP configuration is OK."
        ok = send_email(subj, body, body_html=f"<p>{body}</p>", dry_run=args.dry_run)
        logger.info("Test email result: %s", ok)
        return

    if args.once:
        cnt = process_once(limit=args.limit or None, dry_run=args.dry_run, prune_days=(args.prune_days or 0))
        logger.info("Done. Sent: %d", cnt)
        return

    if args.watch:
        logger.info("Watching… interval=%d min", CHECK_INTERVAL_MINUTES)
        try:
            while True:
                cnt = process_once(limit=args.limit or None, dry_run=args.dry_run, prune_days=(args.prune_days or 0))
                logger.info("Cycle done. Sent: %d", cnt)
                time.sleep(CHECK_INTERVAL_MINUTES * 60)
        except KeyboardInterrupt:
            logger.info("Stopped by user.")
            return

    # default: once
    cnt = process_once(limit=args.limit or None, dry_run=args.dry_run, prune_days=(args.prune_days or 0))
    logger.info("Done. Sent: %d", cnt)

if __name__ == "__main__":
    main()