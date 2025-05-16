from sheet_writer import update_status
from config import ADMINS
from lang import lang_dict

def register_callback_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data.startswith("status_"))
    def handle_status_change(call):
        try:
            parts = call.data.split("_")
            tracking_id = parts[1]
            new_status = parts[2]

            update_status(tracking_id, new_status)

            # Xabarni o‘chirib yuborish yoki tugmalarni yo‘qotish
            bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

            # Admin uchun tasdiq
            bot.answer_callback_query(call.id, text=f"Status yangilandi: {new_status}")

            # Agentga xabar (agar kerak bo‘lsa)
            # bot.send_message(agent_chat_id, f"Tracking ID {tracking_id} uchun status: {new_status}")

        except Exception as e:
            bot.answer_callback_query(call.id, text="Xatolik yuz berdi")
