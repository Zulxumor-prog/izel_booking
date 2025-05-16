import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from config import SHEET_ID, TOKEN
import telebot

# Telegram botni ishga tushirish
bot = telebot.TeleBot(TOKEN)

# Google Sheets ulanish
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

def check_pending():
    rows = sheet.get_all_records()
    for row in rows:
        status = row.get("status", "").lower()
        date_str = row.get("sana", "")
        chat_id = row.get("telegram_id", "")
        if status == "kutilyapti" and chat_id:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                delta = (datetime.now().date() - date_obj).days
                if delta > 2:
                    bot.send_message(int(chat_id), f"⚠️ {row['client_name']} uchun to‘lov hali amalga oshirilmagan.")
            except:
                continue

# Cron orqali ishga tushganda chaqiriladi
if __name__ == "__main__":
    check_pending()
