import asyncio
import feedparser
from deep_translator import GoogleTranslator
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import os
import yagmail

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

translator = GoogleTranslator(source='auto', target='fa')
seen_links = set()

FEEDS = [
    "https://www.animenewsnetwork.com/news/rss.xml",
    "https://www.crunchyroll.com/news/rss",
]

def send_email(subject, body):
    try:
        yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASSWORD)
        yag.send(to=TO_EMAIL, subject=subject, contents=body)
        print("ایمیل فرستاده شد!")
        return True
    except Exception as e:
        print("خطا در ارسال ایمیل:", e)
        return False

async def check_news():
    print(f"[{datetime.now().strftime('%H:%M')}] دارم اخبار رو چک می‌کنم...")
    found = 0

    for url in FEEDS:
        feed = feedparser.parse(url)
        print(f"منبع: {url} | تعداد خبر: {len(feed.entries)}")
        
        for entry in feed.entries[:12]:
            title = entry.title.lower()
            
            if "one piece" not in title and "bounty rush" not in title and "opbr" not in title:
                continue
            
            link = entry.link
            if link in seen_links:
                continue
            
            seen_links.add(link)
            found += 1
            
            fa_title = translator.translate(entry.title)
            summary = entry.get("summary", "")[:400]
            fa_summary = translator.translate(summary) if summary else ""
            
            subject = f"🏴‍☠️ خبر وان‌پیس: {fa_title[:55]}"
            body = f"""{fa_title}

{fa_summary}

منبع: {link}
زمان: {datetime.now().strftime('%Y/%m/%d - %H:%M')}
"""
            send_email(subject, body)

    print(f"تعداد خبر جدید پیدا شده: {found}")
    
    # همیشه یک ایمیل تست بفرست تا مطمئن بشیم کار می‌کنه
    send_email(
        "تست 
