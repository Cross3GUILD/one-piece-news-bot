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
]

def send_email(subject, body):
    try:
        yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASSWORD)
        yag.send(to=TO_EMAIL, subject=subject, contents=body)
        print("ایمیل فرستاده شد!")
    except Exception as e:
        print("خطا در ارسال ایمیل:", e)

async def check_news():
    print(f"[{datetime.now().strftime('%H:%M')}] دارم اخبار رو چک می‌کنم...")

    for url in FEEDS:
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:8]:
            title = entry.title.lower()
            
            if "one piece" not in title and "bounty rush" not in title:
                continue
            
            link = entry.link
            if link in seen_links:
                continue
            
            seen_links.add(link)
            
            fa_title = translator.translate(entry.title)
            summary = entry.get("summary", "")[:400]
            fa_summary = translator.translate(summary) if summary else ""
            
            subject = f"خبر جدید وان‌پیس: {fa_title[:60]}"
            body = f"""{fa_title}

{fa_summary}

منبع: {link}

زمان: {datetime.now().strftime('%Y/%m/%d - %H:%M')}
"""
            send_email(subject, body)

async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_news, "interval", minutes=30)
    scheduler.start()
    
    print("ربات ایمیلی روشن شد...")
    await check_news()
    
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
