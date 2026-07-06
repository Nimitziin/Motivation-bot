import asyncio
import schedule
import time
import threading
import requests
import base64
import os
from datetime import datetime
import pytz

# ── Config ──
BOT_TOKEN = "8952674633:AAFOVr-gEGxagbzt7D2fwTXY44tAw1nLQ4c"
CHAT_ID = "539829626"
TIMEZONE = "Asia/Jerusalem"

# Photo encoded as base64 so it's self-contained
PHOTO_B64 = open("motivation.jpg", "rb").read() if os.path.exists("motivation.jpg") else None

MORNING_MSG = "💪 This is where you want to be.\n\nStay on track with your nutrition today. You've got this."
EVENING_MSG = "💪 This is where you want to be.\n\nHow did your nutrition go today? Finish strong — every choice counts."

def send_photo_message(caption):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    if PHOTO_B64:
        files = {"photo": ("motivation.jpg", open("motivation.jpg", "rb"), "image/jpeg")}
        data = {"chat_id": CHAT_ID, "caption": caption}
        r = requests.post(url, files=files, data=data)
    else:
        url2 = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url2, data={"chat_id": CHAT_ID, "text": caption})
    print(f"[{datetime.now()}] Sent: {r.status_code}")

def morning_reminder():
    send_photo_message(MORNING_MSG)

def evening_reminder():
    send_photo_message(EVENING_MSG)

def run_scheduler():
    tz = pytz.timezone(TIMEZONE)
    
    schedule.every().day.at("10:00").do(morning_reminder)
    schedule.every().day.at("20:30").do(evening_reminder)
    
    print(f"Bot running. Scheduled 10:00 AM and 8:30 PM ({TIMEZONE})")
    
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    # Send a startup confirmation
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": "✅ Your motivation bot is live! You'll receive reminders at 10:00 AM and 8:30 PM every day."}
    )
    run_scheduler()
