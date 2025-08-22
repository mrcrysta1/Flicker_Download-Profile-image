<<<<<<< HEAD
# Pakistan Trading & SECP Alerts → Email (Roman Urdu)

Ye script RSS/news sources ko watch karta hai aur jab nayi khabar mile to **short Roman Urdu** summary bana kar **Gmail** se email karta hai.

## Features
- SECP, Dawn, The News, ProPakistani jaisi sources ko check karta hai
- AI se **short Roman Urdu** summary (OpenAI **ya** Groq; optional & free-tier possible). Agar API key na ho to basic fallback summary bhej deta hai.
- Duplicate emails avoid (local `seen.json` store)
- CLI options: one-off run **ya** continuous watch mode

## Setup (Quick)
1. **Python 3.9+** install hona chahiye.
2. Ye files download karo (ye folder): `/mnt/data/news_alert_email`
3. Terminal me:
   ```bash
   cd "/mnt/data/news_alert_email"
   pip install -r requirements.txt
   cp .env.example .env
   ```
4. `.env` file me apna Gmail or App Password set karo (niche guide). Optionally AI key bhee:
   - `OPENAI_API_KEY` **ya** `GROQ_API_KEY` (agar chaho to free tier try karo)
5. Test run:
   ```bash
   python monitor_news.py --once
   ```
6. Continuous watch (30 min interval by default):
   ```bash
   python monitor_news.py --watch
   ```

## Gmail SMTP (App Password)
- Gmail me **2-Step Verification (2FA)** ON karo.
- **App Password** create karo: Google Account → Security → App passwords → “Mail” on “Other/Custom (Python)”.
- `.env` me `EMAIL_ADDRESS` aur `EMAIL_APP_PASSWORD` set karo.
- `TO_EMAIL` me apna email likho jahan alerts chahiyen.

## Sources (Editable)
- SECP Press Releases (scrape)
- Dawn Business RSS
- The News Business RSS
- ProPakistani (Business/Finance) RSS

Aap `/mnt/data/news_alert_email/monitor_news.py` me `SOURCE_FEEDS` aur `SECP_PRESS_URL` change/add kar sakte ho.

## Windows Auto Start (Task Scheduler)
- Task Scheduler → Create Task → Trigger: At logon/repeat 30min → Action: `python monitor_news.py --watch`

## Linux/Mac (cron) example
```
*/30 * * * * /usr/bin/python3 /mnt/data/news_alert_email/monitor_news.py --once
```

## Legal & Safety
- Ye sirf **public information** monitor karta hai.
- AI summary optional hai; aap free/local models bhi laga sakte ho.

— Made for Ali (Roman Urdu alerts) ♥
=======
# Flicker_Download-Profile-image
>>>>>>> 1ef247c9d8c7fb97937a539adec6ec5489711c83
