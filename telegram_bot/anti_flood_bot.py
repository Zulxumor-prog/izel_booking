import telebot
from telebot import types
import time

# Token va boshqa sozlamalar
TOKEN = '7927590527:AAHu1eG-cDV_DHoiHim78G00VxaDl06a_84'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    try:
        bot.send_message(chat_id, "Bot ishga tushdi.")
        time.sleep(1.5)
    except telebot.apihelper.ApiTelegramException as e:
        if "Too Many Requests" in str(e):
            time.sleep(10)
            bot.send_message(chat_id, "Iltimos, biroz kuting... Telegram cheklovi.")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    try:
        bot.send_message(call.message.chat.id, "Callback tugmasi bosildi.")
        time.sleep(1.5)
    except telebot.apihelper.ApiTelegramException as e:
        if "Too Many Requests" in str(e):
            time.sleep(10)
            bot.send_message(call.message.chat.id, "Callback cheklovga tushdi.")

bot.polling(non_stop=True)
