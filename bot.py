import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Load cadet data from files
def load_cadets():
    cadets = {}
    folder = "cadets"
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            with open(os.path.join(folder, filename), "r", encoding="utf-8") as file:
                cadets[filename.replace("info_", "").replace(".txt", "")] = file.read()
    return cadets

CADETS = list(load_cadets().keys())
CADETS_PER_PAGE = 6  # Adjust number of cadets per page

# Home page handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("👥 ᴠɪᴇᴡ ᴄᴀᴅᴇᴛs", callback_data="view_cadets_0")]]
    await update.message.reply_text(
        "☁️ ᴡᴇ ᴀʀᴇ ᴛʜᴇ sᴄᴏᴜᴛ ʀᴇɢɪᴍᴇɴᴛ ☁️\n\n"
        "☄️ ғɪɢʜᴛɪɴɢ ғᴏʀ ʜᴜᴍᴀɴɪᴛʏ's ғʀᴇᴇᴅᴏᴍ\n"
        "⚔️ ᴅᴇғᴇᴀᴛɪɴɢ ᴛɪᴛᴀɴs ᴀɴᴅ ᴇxᴘʟᴏʀɪɴɢ ᴛʜᴇ ᴡᴏʀʟᴅ\n\n"
        "🚀 ᴊᴏɪɴ ᴜs ᴀɴᴅ ʜᴏɴᴏʀ ᴛʜᴇ ᴄᴀᴅᴇᴛs!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Generate paginated cadet list
def get_cadet_keyboard(page: int):
    start_index = page * CADETS_PER_PAGE
    end_index = start_index + CADETS_PER_PAGE
    paginated_cadets = CADETS[start_index:end_index]

    keyboard = []
    row = []
    for i, cadet in enumerate(paginated_cadets, 1):
        row.append(InlineKeyboardButton(cadet.replace("_", " "), callback_data=f"cadet_{cadet}"))
        if i % 3 == 0:  # 3 cadets per row
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    # Pagination Buttons
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data=f"view_cadets_{page - 1}"))
    if end_index < len(CADETS):
        nav_buttons.append(InlineKeyboardButton("➡️ ɴᴇxᴛ", callback_data=f"view_cadets_{page + 1}"))

    keyboard.append(nav_buttons)  # Add pagination buttons
    keyboard.append([InlineKeyboardButton("🏠 ʜᴏᴍᴇ", callback_data="home")])
    
    return InlineKeyboardMarkup(keyboard)

# View cadets with pagination
async def view_cadets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    page = int(query.data.split("_")[-1])
    await query.answer()
    await query.edit_message_text("🌟 ᴄʜᴏᴏsᴇ ᴀ ᴄᴀᴅᴇᴛ 🌟", reply_markup=get_cadet_keyboard(page))

# Show cadet details
async def show_cadet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    cadet_name = query.data.replace("cadet_", "")
    keyboard = [[InlineKeyboardButton("⬅️ ʙᴀᴄᴋ", callback_data="view_cadets_0")]]
    await query.answer()
    await query.edit_message_text(f"📝 **{cadet_name.replace('_', ' ')}**\n\n{CADETS[cadet_name]}", reply_markup=InlineKeyboardMarkup(keyboard))

# Button handlers
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data.startswith("view_cadets_"):
        await view_cadets(update, context)
    elif query.data == "home":
        await start(update, context)
    elif query.data.startswith("cadet_"):
        await show_cadet(update, context)

# Main function
def main():
    app = ApplicationBuilder().token("7840330195:AAGrqH2CBndzHIChGRa3WtSyEy7Bj-aJZOI").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
