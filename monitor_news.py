import os, time, json, re, argparse, textwrap, hashlib
from datetime import datetime, timezone
from email.message import EmailMessage

import requests
import feedparser
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# --- Load env
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")
CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "30"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Storage for de-dup
SEEN_PATH = os.path.join(os.path.dirname(__file__), "seen.json")
def load_seen():
    if os.path.exists(SEEN_PATH):
        try:
            return json.load(open(SEEN_PATH, "r", encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_seen(seen):
    with open(SEEN_PATH, "w", encoding="utf-8") as f:
        json.dump(seen, f, ensure_ascii=False, indent=2)

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

def hash_id(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def fetch_secp_press():
    """Scrape SECP press releases page and return list of dicts: [{'title','link','summary'}]"""
    items = []
    try:
        r = requests.get(SECP_PRESS_URL, headers=HEADERS, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # The SECP site layout may change; try to find article cards/links
        for a in soup.select("a"):
            href = a.get("href", "")
            text = (a.get_text() or "").strip()
            if not href or not text:
                continue
            # Heuristic: pick links that look like press releases (contain /press-release/ or /media-center/)
            if "press" in href or "media-center" in href:
                # Normalize absolute link
                if href.startswith("/"):
                    link = "https://www.secp.gov.pk" + href
                else:
                    link = href
                # Deduplicate by title+link
                key = hash_id(text + "|" + link)
                items.append({"title": text, "link": link, "summary": "" , "id": key})
        # Simple unique by id
        uniq = {}
        for it in items:
            uniq[it["id"]] = it
        return list(uniq.values())
    except Exception as e:
        print("[warn] SECP fetch failed:", e)
        return []

def fetch_rss(url):
    out = []
    try:
        feed = feedparser.parse(url)
        for e in feed.entries[:20]:
            title = e.get("title", "").strip()
            link = e.get("link", "").strip()
            summary = (e.get("summary", "") or "").strip()
            key = hash_id(title + "|" + link)
            out.append({"title": title, "link": link, "summary": summary, "id": key})
    except Exception as e:
        print(f"[warn] RSS failed {url}:", e)
    return out

def collect_items():
    items = []
    items.extend(fetch_secp_press())
    for f in SOURCE_FEEDS:
        items.extend(fetch_rss(f))
    # De-dup by id
    uniq = {}
    for it in items:
        uniq[it["id"]] = it
    return list(uniq.values())

# --- AI Summarizer (Roman Urdu)
def ai_summarize_roman(text, title):
    prompt = f"""
Summarize the following news for a Pakistani audience in 2 short lines **in Roman Urdu**, very simple and casual.
Keep only the key fact (who/what) + action (ban/warning/job/report) + when (if present) + what to do (avoid/join/apply).
No formal Urdu script; ONLY Roman Urdu.
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
            print("[warn] OpenAI failed:", e)

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
            print("[warn] Groq failed:", e)

    # Fallback: simple heuristic shortener + manual romanization-lite
    text = re.sub(r"\s+", " ", text)
    text = text[:300]
    baselines = [
        "update aayi hai",
        "important khabar hai",
        "zaroor check karein",
        "details link me",
    ]
    return f"{title[:60]} — ye important update hai, details link me dekh lo. {baselines[0]}"

# --- Email
def send_email(subject, body):
    import smtplib, ssl
    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD or not TO_EMAIL:
        print("[error] EMAIL env not set. Skipping email.")
        return False
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        smtp.send_message(msg)
    return True

def format_email(item, roman_summary):
    lines = [
        f"**Title:** {item['title']}",
        "",
        f"**Roman Urdu Summary:**",
        roman_summary,
        "",
        f"Source: {item['link']}",
        f"Time: {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}",
    ]
    return "\n".join(lines)

def process_once():
    global seen
    items = collect_items()
    sent = 0
    for it in items:
        if it["id"] in seen:
            continue
        # Build text for AI
        text_for_ai = it["summary"] or it["title"]
        roman = ai_summarize_roman(text_for_ai, it["title"])
        email_body = format_email(it, roman)
        subj = f"[Alert] {it['title'][:70]}"
        ok = send_email(subj, email_body)
        if ok:
            seen[it["id"]] = {"ts": time.time(), "title": it["title"]}
            sent += 1
            print("[sent]", it["title"])
        else:
            print("[skip] email not configured.")
    if sent:
        save_seen(seen)
    return sent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="Run one scan and exit")
    ap.add_argument("--watch", action="store_true", help="Run in a loop (interval from env)")
    args = ap.parse_args()

    if args.once:
        cnt = process_once()
        print(f"Done. Sent: {cnt}")
        return

    if args.watch:
        print(f"Watching… interval={CHECK_INTERVAL_MINUTES} min")
        try:
            while True:
                cnt = process_once()
                print(f"Cycle done. Sent: {cnt}")
                time.sleep(CHECK_INTERVAL_MINUTES * 60)
        except KeyboardInterrupt:
            print("Stopped by user.")
            return

    # default: once
    cnt = process_once()
    print(f"Done. Sent: {cnt}")

if __name__ == "__main__":
    main()