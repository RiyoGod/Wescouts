import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Bot Token (Replace with your actual token)
BOT_TOKEN = "7782893047:AAHszTxJ4IE7lkidNBpVA3xI0hYDOv_ed4A"

# Cadets Data
CADETS = {
    "Mikasa Ackerman": "ᴇʟɪᴛᴇ sᴄᴏᴜᴛ, ᴇxᴄᴇᴘᴛɪᴏɴᴀʟ sᴋɪʟʟs, ᴅᴇᴅɪᴄᴀᴛᴇᴅ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛɪɴɢ ᴇʀᴇɴ.",
    "Armin Arlert": "ʙʀɪʟʟɪᴀɴᴛ ᴛᴀᴄᴛɪᴄɪᴀɴ, ᴜsᴇs ɪɴᴛᴇʟʟɪɢᴇɴᴄᴇ ᴏᴠᴇʀ sᴛʀᴇɴɢᴛʜ.",
    "Jean Kirstein": "ʀᴇᴀʟɪsᴛɪᴄ ʟᴇᴀᴅᴇʀ, ᴛʜʀɪᴠᴇs ᴜɴᴅᴇʀ ᴘʀᴇssᴜʀᴇ.",
    "Connie Springer": "ʟᴏʏᴀʟ ᴀɴᴅ ᴅᴇᴅɪᴄᴀᴛᴇᴅ, ʀᴇᴍᴀɪɴs ᴏᴘᴛɪᴍɪsᴛɪᴄ.",
    "Sasha Blouse": "ᴇxᴄᴇʟʟᴇɴᴛ ᴍᴀʀᴋsᴍᴀɴ, ᴄᴏᴜʀᴀɢᴇᴏᴜs ᴀɴᴅ ᴄᴀʀᴇғʀᴇᴇ.",
    "Levi Ackerman": "ʜɪsᴛᴏʀʏ's sᴛʀᴏɴɢᴇsᴛ sᴄᴏᴜᴛ, ᴜɴʀɪᴠᴀʟᴇᴅ ɪɴ ᴄᴏᴍʙᴀᴛ."
}

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("ᴠɪᴇᴡ ᴏᴜʀ ᴄᴀᴅᴇᴛs", callback_data="view_cadets")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "⚔️ ᴛʜᴇ sᴄᴏᴜᴛ ʀᴇɢɪᴍᴇɴᴛ ⚔️\n\n"
        "ʀᴇᴠᴏʟᴜᴛɪᴏɴ ʙʀᴏᴜɢʜᴛ ʙʏ ᴛʜᴏsᴇ ᴡʜᴏ ᴅᴀʀᴇ ᴛᴏ ғɪɢʜᴛ.\n\n"
        "ᴊᴏɪɴ ᴏᴜʀ ᴄᴀᴅᴇᴛs ɪɴ ᴛʜᴇ ʙᴀᴛᴛʟᴇ ғᴏʀ ʜᴜᴍᴀɴɪᴛʏ!",
        reply_markup=reply_markup
    )

# View Cadets
async def view_cadets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    buttons = []
    cadet_names = list(CADETS.keys())

    for i in range(0, len(cadet_names), 2):  # 2x3 Grid Layout
        row = [InlineKeyboardButton(cadet_names[i], callback_data=f"cadet_{cadet_names[i]}")]
        if i + 1 < len(cadet_names):
            row.append(InlineKeyboardButton(cadet_names[i + 1], callback_data=f"cadet_{cadet_names[i + 1]}"))
        buttons.append(row)

    buttons.append([InlineKeyboardButton("🔙 ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ᴍᴇɴᴜ", callback_data="back_to_main")])

    reply_markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text("🔹 **Sᴄᴏᴜᴛ Rᴇɢɪᴍᴇɴᴛ Cᴀᴅᴇᴛs** 🔹", reply_markup=reply_markup)

# Cadet Details
async def cadet_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    cadet_name = query.data.replace("cadet_", "")
    info = CADETS.get(cadet_name, "Nᴏ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀᴠᴀɪʟᴀʙʟᴇ.")

    buttons = [
        [InlineKeyboardButton("🔙 ʙᴀᴄᴋ ᴛᴏ ᴄᴀᴅᴇᴛs", callback_data="view_cadets")]
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    await query.edit_message_text(f"**{cadet_name}**\n\n{info}", reply_markup=reply_markup)

# Back to Main Menu
async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("ᴠɪᴇᴡ ᴏᴜʀ ᴄᴀᴅᴇᴛs", callback_data="view_cadets")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        "⚔️ ᴛʜᴇ sᴄᴏᴜᴛ ʀᴇɢɪᴍᴇɴᴛ ⚔️\n\n"
        "ʀᴇᴠᴏʟᴜᴛɪᴏɴ ʙʀᴏᴜɢʜᴛ ʙʏ ᴛʜᴏsᴇ ᴡʜᴏ ᴅᴀʀᴇ ᴛᴏ ғɪɢʜᴛ.\n\n"
        "ᴊᴏɪɴ ᴏᴜʀ ᴄᴀᴅᴇᴛs ɪɴ ᴛʜᴇ ʙᴀᴛᴛʟᴇ ғᴏʀ ʜᴜᴍᴀɴɪᴛʏ!",
        reply_markup=reply_markup
    )

# Main Function
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(view_cadets, pattern="view_cadets"))
    app.add_handler(CallbackQueryHandler(cadet_details, pattern="cadet_"))
    app.add_handler(CallbackQueryHandler(back_to_main, pattern="back_to_main"))

    app.run_polling()

if __name__ == "__main__":
    main()
