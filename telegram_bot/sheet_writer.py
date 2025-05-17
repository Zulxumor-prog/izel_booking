import gspread
import json 
import os
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from django.conf import settings 
SHEET_ID = settings.GOOGLE_SHEET_ID

# 1. Google Sheets ulanishi
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_json = os.environ.get("GOOGLE_CREDENTIALS")  # Render environment'dan
credentials_dict = json.loads(credentials_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).sheet1

# 2. Google Sheets’ga yozish
def write_to_sheet(data):
    today = datetime.now().strftime("%Y-%m-%d")
    sheet.append_row([
        data.get("client_name", ""),
        data.get("phone", ""),
        data.get("route", ""),
        data.get("passport_link", ""),
        data.get("photo_link", ""),
        data.get("receipt_link", ""),
        "Yangi",  # status
        data.get("tracking_id", ""),
        data.get("telegram_id", ""),
        today
    ])

# 3. Statusni yangilash
def update_status(tracking_id, new_status):
    records = sheet.get_all_records()
    for i, row in enumerate(records):
        if row.get("tracking_id") == tracking_id:
            sheet.update_cell(i + 2, 7, new_status)  # status ustuni
            break
