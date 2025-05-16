from telebot import types
from config import ADMINS
from pdf_generator import generate_pdf

def register_admin_handlers(bot, sheet):
    @bot.message_handler(commands=['admin'])
    def admin_menu(message):
        if message.chat.id not in ADMINS:
            bot.send_message(message.chat.id, "❌ Sizda ruxsat yo‘q.")
            return
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("/statistika", "/list", "/pdf")
        bot.send_message(message.chat.id, "📊 Admin menyu:", reply_markup=markup)

    @bot.message_handler(commands=['statistika'])
    def show_stats(message):
        if message.chat.id not in ADMINS:
            return
        data = sheet.get_all_records()
        agent_counts = {}
        for row in data:
            agent = row.get('telegram_id')
            if agent:
                agent_counts[agent] = agent_counts.get(agent, 0) + 1
        text = "\n".join([f"{k}: {v} ta mijoz" for k, v in agent_counts.items()])
        bot.send_message(message.chat.id, "📈 Statistika:\n" + (text or "Ma'lumot topilmadi"))

    @bot.message_handler(commands=['list'])
    def list_recent(message):
        if message.chat.id not in ADMINS:
            return
        data = sheet.get_all_records()[-5:]
        text = "\n\n".join([f"{r['client_name']} — {r['route']} ({r['status']})" for r in data])
        bot.send_message(message.chat.id, "🧾 Oxirgi 5 mijoz:\n" + text)

    @bot.message_handler(commands=['pdf'])
    def send_pdf(message):
        if message.chat.id not in ADMINS:
            return
        pdf_path = generate_pdf(sheet)
        with open(pdf_path, 'rb') as f:
            bot.send_document(message.chat.id, f)
