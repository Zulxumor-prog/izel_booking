import telebot
from telebot import types
from datetime import datetime
import os
import time
import gspread

from oauth2client.service_account import ServiceAccountCredentials
from config import TOKEN, GROUP_ID, ALLOWED_USERS, PDF_FOLDER_PATH
from lang import lang_dict
from drive_uploader import upload_files_to_drive
from sheet_writer import write_to_sheet
from pdf_chek import generate_chek
from utils import generate_tracking_id, save_file, generate_qr
from log_manager import log_error
from callback_handler import register_callback_handlers
from admin_panel import register_admin_handlers

# Google Sheets sozlamasi
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials/izel-agent.json', scope)
gc = gspread.authorize(creds)
sheet = gc.open_by_key('1Juz_Tn8lPsY8Ozn7eICPitArMggWBnjx8xuNT49EKsI').sheet1

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    if message.chat.type != 'private':
        return
    if chat_id not in ALLOWED_USERS:
        return bot.send_message(chat_id, "❌ Sizga ruxsat yo‘q.")

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🇺🇿 O‘zbek", callback_data='lang_uz'),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')
    )
    bot.send_message(chat_id, "Tilni tanlang:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def set_language(call):
    chat_id = call.message.chat.id
    lang = call.data.split("_")[1]
    user_data[chat_id] = {'lang': lang, 'step': 'client_name'}
    bot.send_message(chat_id, lang_dict[lang]['client_name'])

@bot.message_handler(func=lambda m: user_data.get(m.chat.id, {}).get('step') == 'client_name')
def ask_phone(message):
    chat_id = message.chat.id
    user_data[chat_id]['client_name'] = message.text
    user_data[chat_id]['step'] = 'phone'
    lang = user_data[chat_id]['lang']
    bot.send_message(chat_id, lang_dict[lang]['phone'])

@bot.message_handler(func=lambda m: user_data.get(m.chat.id, {}).get('step') == 'phone')
def ask_route(message):
    chat_id = message.chat.id
    user_data[chat_id]['phone'] = message.text
    user_data[chat_id]['step'] = 'route'
    lang = user_data[chat_id]['lang']
    markup = types.InlineKeyboardMarkup()
    routes = ["Horgos", "Urumchi", "Guanchjou", "Yiwu"]
    for r in routes:
        markup.add(types.InlineKeyboardButton(r, callback_data=f"route_{r}"))
    bot.send_message(chat_id, lang_dict[lang]['route'], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("route_"))
def save_route(call):
    chat_id = call.message.chat.id
    route = call.data.split("_")[1]
    lang = user_data[chat_id]['lang']
    user_data[chat_id]['route'] = route
    user_data[chat_id]['step'] = 'passport'
    bot.send_message(chat_id, lang_dict[lang]['passport'])
    bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['text'])
def fallback_text(message):
    if message.chat.type != 'private':
        return
    chat_id = message.chat.id
    step = user_data.get(chat_id, {}).get('step')
    if step:
        return
    bot.send_message(chat_id, "Iltimos, /start buyrug‘ini bosing.")

@bot.message_handler(content_types=['document', 'photo'])
def handle_files(message):
    chat_id = message.chat.id
    if chat_id not in user_data or 'step' not in user_data[chat_id]:
        return

    lang = user_data[chat_id]['lang']
    step = user_data[chat_id]['step']

    try:
        file_id = message.document.file_id if message.document else message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        filename = message.document.file_name if message.document else f"{step}_{datetime.now().timestamp()}.jpg"

        if message.document and message.document.file_size > 5 * 1024 * 1024:
            bot.send_message(chat_id, "⚠️ Fayl 5MB dan oshmasligi kerak.")
            return

        file_bytes = bot.download_file(file_info.file_path)
        path = save_file(step, filename, file_bytes)
        user_data[chat_id][step] = path

        next_order = ['passport', 'photo', 'receipt']
        if step in next_order:
            next_index = next_order.index(step) + 1
            if next_index < len(next_order):
                user_data[chat_id]['step'] = next_order[next_index]
                bot.send_message(chat_id, lang_dict[lang][next_order[next_index]])
            else:
                user_data[chat_id]['step'] = 'done'
                bot.send_message(chat_id, lang_dict[lang]['uploading'])

                user_data[chat_id]['tracking_id'] = generate_tracking_id()
                user_data[chat_id]['qr_path'] = generate_qr(user_data[chat_id]['tracking_id'])
                user_data[chat_id]['telegram_id'] = chat_id

                links = upload_files_to_drive(user_data[chat_id])
                user_data[chat_id].update(links)
                write_to_sheet(user_data[chat_id])

                pdf_path = os.path.join(PDF_FOLDER_PATH, f"chek_{user_data[chat_id]['tracking_id']}.pdf")
                generate_chek(user_data[chat_id], pdf_path)

                with open(pdf_path, 'rb') as f:
                    bot.send_document(chat_id, f)

                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton("✅ Qabul qilindi", callback_data=f"status_{user_data[chat_id]['tracking_id']}_accepted"),
                    types.InlineKeyboardButton("❌ Bekor qilindi", callback_data=f"status_{user_data[chat_id]['tracking_id']}_rejected")
                )

                username = message.from_user.username or f"id: {chat_id}"

                msg = f"""📌 Yangi mijoz:
👤 Ismi: {user_data[chat_id]['client_name']}
📞 Telefon: {user_data[chat_id]['phone']}
🗺 Yo‘nalish: {user_data[chat_id]['route']}
👤 Agent: @{username}
🔢 ID: {user_data[chat_id]['tracking_id']}"""

                bot.send_message(GROUP_ID, msg, reply_markup=markup)

                # Fayllarni guruhga yuborish
                for file_key in ['passport', 'photo', 'receipt']:
                    if file_key in user_data[chat_id]:
                        with open(user_data[chat_id][file_key], 'rb') as f:
                            bot.send_document(GROUP_ID, f)

                bot.send_message(chat_id, lang_dict[lang]['done'])
                user_data.pop(chat_id)

    except Exception as e:
        log_error(chat_id, str(e))
        bot.send_message(chat_id, f"Xatolik: {e}")

# Callback va admin handlerlar
register_callback_handlers(bot)
register_admin_handlers(bot, sheet)

# Botni ishga tushirish
bot.polling(non_stop=True, timeout=90)
