import os
import time
import requests
from bs4 import BeautifulSoup

# Telegram Info
BOT_TOKEN = "7608203253:AAExlG6YjLqNET2v0mFX4ouWzHyONjTsmbE"
CHAT_ID = "-1002784088755"

# iVasms Session Cookie
COOKIE = "ivas_sms_session=eyJpdiI6InN0UEpjMngwaGh0MVF1SmtJQ0JtNHc9PSIsInZhbHVlIjo...; XSRF-TOKEN=eyJpdiI6InN0UEpjMngwaGh0MVF1SmtJQ0JtNHc9PSIsInZhbHVlIjo..."

URL = "https://www.ivasms.com/portal/live/my_sms"
HEADERS = {
    "Cookie": COOKIE,
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest"
}

# Save seen OTPs by (number + otp text)
seen_otps = set()

def get_latest_sms():
    try:
        res = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select("table tbody tr")

        for row in rows:
            cols = [td.text.strip() for td in row.find_all("td")]
            if len(cols) < 7:
                continue

            number = cols[2]
            otp = cols[6]

            unique_key = f"{number}_{otp}"
            if unique_key in seen_otps:
                continue

            seen_otps.add(unique_key)

            msg = f"New OTP Detected ✅\n\nNumber   : {number}\nOTP Code : {otp}"
            send_to_telegram(msg)
    except Exception as e:
        print("Error:", e)

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=data)

# Run loop
while True:
    get_latest_sms()
    time.sleep(20)
