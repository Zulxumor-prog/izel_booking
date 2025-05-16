from datetime import datetime

def log_error(chat_id, error):
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] ChatID: {chat_id} | Xatolik: {error}\n")
