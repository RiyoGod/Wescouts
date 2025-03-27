import logging
import pytz
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# **Replace this with your actual bot token**
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Timezone configuration
timezone = pytz.utc  # Change to your preferred timezone if needed
scheduler = AsyncIOScheduler(timezone=timezone)

# **Cadet Details**
CADETS = {
    "eren": "🔹 ᴇʀᴇɴ ʏᴇᴀɢᴇʀ 🔹\n\n- ᴛʜᴇ ᴄᴏʀᴇ ғɪɢʜᴛᴇʀ ᴏғ ʜᴜᴍᴀɴɪᴛʏ.\n- ʜᴇ ʙᴇᴄᴀᴍᴇ ᴀ ᴛɪᴛᴀɴ ᴀɴᴅ ғᴏᴜɢʜᴛ ғᴏʀ ғʀᴇᴇᴅᴏᴍ.",
    "mikasa": "🔹 ᴍɪᴋᴀsᴀ ᴀᴄᴋᴇʀᴍᴀɴ 🔹\n\n- ᴛʜᴇ sᴛʀᴏɴɢᴇsᴛ sᴄᴏᴜᴛ.\n- ᴀʟᴡᴀʏs ᴘʀᴏᴛᴇᴄᴛɪɴɢ ᴇʀᴇɴ.",
    "armin": "🔹 ᴀʀᴍɪɴ ᴀʀʟᴇʀᴛ 🔹\n\n- ᴀ ɢᴇɴɪᴜs sᴛʀᴀᴛᴇɢɪsᴛ.\n- ᴜsᴇᴅ ʜɪs ɪɴᴛᴇʟʟᴇᴄᴛ ᴛᴏ sᴀᴠᴇ ᴍᴀɴʏ ʟɪᴠᴇs.",
    "levi": "🔹 ʟᴇᴠɪ ᴀᴄᴋᴇʀᴍᴀɴ 🔹\n\n- ᴛʜᴇ sᴛʀᴏɴɢᴇsᴛ ᴄᴀᴘᴛᴀɪɴ.\n- ʜɪs ᴛɪᴛᴀɴ-ᴋɪʟʟɪɴɢ sᴋɪʟʟs ᴀʀᴇ ᴜɴᴍᴀᴛᴄʜᴇᴅ.",
    "hange": "🔹 ʜᴀɴɢᴇ ᴢᴏᴇ 🔹\n\n- ᴛʜᴇ ɪɴᴛᴇʟʟɪɢᴇɴᴛ ʀᴇsᴇᴀʀᴄʜᴇʀ.\n- ᴅᴇᴠᴏᴛᴇᴅ ᴛᴏ ᴜɴᴅᴇʀsᴛᴀɴᴅɪɴɢ ᴛɪᴛᴀɴs.",
    "jean": "🔹 ᴊᴇᴀɴ ᴋɪʀsᴛᴇɪɴ 🔹\n\n- ʙᴇᴄᴀᴍᴇ ᴀ ʟᴇᴀᴅᴇʀ.\n- ғɪɢʜᴛs ғᴏʀ ᴡʜᴀᴛ ɪs ʀɪɢʜᴛ."
}

# **Start Command**
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ᴠɪᴇᴡ ᴏᴜʀ ᴄᴀᴅᴇᴛs", callback_data="view_cadets")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🏅 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ sᴄᴏᴜᴛ ʀᴇɢɪᴍᴇɴᴛ!\n\n"
        "ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴘᴛɪᴏɴ ʙᴇʟᴏᴡ:",
        reply_markup=reply_markup
    )

# **Handle Inline Button Clicks**
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "view_cadets":
        keyboard = [
            [InlineKeyboardButton("ᴇʀᴇɴ ʏᴇᴀɢᴇʀ", callback_data="eren"),
             InlineKeyboardButton("ᴍɪᴋᴀsᴀ ᴀᴄᴋᴇʀᴍᴀɴ", callback_data="mikasa")],
            [InlineKeyboardButton("ᴀʀᴍɪɴ ᴀʀʟᴇʀᴛ", callback_data="armin"),
             InlineKeyboardButton("ʟᴇᴠɪ ᴀᴄᴋᴇʀᴍᴀɴ", callback_data="levi")],
            [InlineKeyboardButton("ʜᴀɴɢᴇ ᴢᴏᴇ", callback_data="hange"),
             InlineKeyboardButton("ᴊᴇᴀɴ ᴋɪʀsᴛᴇɪɴ", callback_data="jean")],
            [InlineKeyboardButton("⬅ ʙᴀᴄᴋ", callback_data="back_home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "🔹 ᴏᴜʀ ᴄᴀᴅᴇᴛs 🔹\n\n"
            "ᴄʜᴏᴏsᴇ ᴀ ᴄᴀᴅᴇᴛ ᴛᴏ ᴠɪᴇᴡ ᴛʜᴇɪʀ ᴄᴏɴᴛʀɪʙᴜᴛɪᴏɴs:",
            reply_markup=reply_markup
        )

    elif query.data in CADETS:
        keyboard = [[InlineKeyboardButton("⬅ ʙᴀᴄᴋ", callback_data="view_cadets")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            CADETS[query.data],
            reply_markup=reply_markup
        )

    elif query.data == "back_home":
        await start(update, context)

# **Main Function**
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(lambda _: scheduler.start()).build()

    # Add Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Run Bot
    app.run_polling()

if __name__ == "__main__":
    main()
