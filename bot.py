import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Load cadet data from files
def load_cadets():
    cadets = {}
    folder = "cadets"
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as file:
                cadets[filename.replace("info_", "").replace(".txt", "")] = file.read()
    return cadets

CADETS = load_cadets()

# Home page handler
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("👥 ᴠɪᴇᴡ ᴄᴀᴅᴇᴛs", callback_data="view_cadets")]]
    update.message.reply_text(
        "☁️ ᴡᴇ ᴀʀᴇ ᴛʜᴇ sᴄᴏᴜᴛ ʀᴇɢɪᴍᴇɴᴛ ☁️\n\n"
        "☄️ ғɪɢʜᴛɪɴɢ ғᴏʀ ʜᴜᴍᴀɴɪᴛʏ's ғʀᴇᴇᴅᴏᴍ\n"
        "⚔️ ᴅᴇғᴇᴀᴛɪɴɢ ᴛɪᴛᴀɴs ᴀɴᴅ ᴇxᴘʟᴏʀɪɴɢ ᴛʜᴇ ᴡᴏʀʟᴅ\n\n"
        "🚀 ᴊᴏɪɴ ᴜs ᴀɴᴅ ʜᴏɴᴏʀ ᴛʜᴇ ᴄᴀᴅᴇᴛs!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# View cadets
def view_cadets(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton(cadet.replace("_", " "), callback_data=f"cadet_{cadet}")] for cadet in CADETS]
    keyboard.append([InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="home")])
    query = update.callback_query
    query.answer()
    query.edit_message_text("🌟 ᴄʜᴏᴏsᴇ ᴀ ᴄᴀᴅᴇᴛ 🌟", reply_markup=InlineKeyboardMarkup(keyboard))

# Show cadet details
def show_cadet(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    cadet_name = query.data.replace("cadet_", "")
    if cadet_name in CADETS:
        keyboard = [[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="view_cadets")]]
        query.answer()
        query.edit_message_text(CADETS[cadet_name], reply_markup=InlineKeyboardMarkup(keyboard))

# Button handlers
def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == "view_cadets":
        view_cadets(update, context)
    elif query.data == "home":
        start(update, context)
    elif query.data.startswith("cadet_"):
        show_cadet(update, context)

# Main function
def main():
    updater = Updater("7782893047:AAHszTxJ4IE7lkidNBpVA3xI0hYDOv_ed4A")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
