from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "7782893047:AAHszTxJ4IE7lkidNBpVA3xI0hYDOv_ed4A"

# Scout Regiment Cadets Data (Name, Description)
cadets = [
    ("Eren Yeager", "The key to humanity's freedom, carrying the will of the Attack Titan."),
    ("Mikasa Ackerman", "A warrior with unmatched skill and devotion to Eren."),
    ("Armin Arlert", "A brilliant strategist with a heart for peace."),
    ("Jean Kirstein", "A leader who evolved from a reluctant soldier to a true hero."),
    ("Connie Springer", "A loyal friend with unshakable courage."),
    ("Sasha Blouse", "A sharp shooter and the heart of the Scouts."),
    ("Historia Reiss", "The true queen of the walls, who chose freedom over royalty."),
    ("Levi Ackerman", "The strongest soldier, humanity’s last hope."),
    ("Hange Zoë", "A scientist obsessed with Titans and leader of the Scouts."),
    ("Erwin Smith", "The visionary commander who led the charge for truth."),
    ("Floch Forster", "A believer in Eldian survival, willing to take extreme measures."),
    ("Keith Shadis", "A former commander who trained the next generation of Scouts."),
    ("Ymir", "A warrior with a mysterious past and deep connection to Historia."),
    ("Petra Ral", "An elite soldier of Levi’s squad, known for her loyalty."),
    ("Oluo Bozado", "A skilled fighter with a strong admiration for Levi."),
    ("Eld Jinn", "A calm and experienced member of Levi's squad."),
    ("Gunther Schultz", "A tactical soldier who fought fearlessly in Levi's squad."),
    ("Moblit Berner", "Hange Zoë's assistant, known for his patience and intelligence."),
    ("Nifa", "A messenger and scout, dedicated to Erwin’s cause."),
    ("Marlowe Freudenberg", "A soldier who questioned authority and sought true justice."),
    ("Hitch Dreyse", "A Military Police soldier who later sympathized with the Scouts."),
    ("Anka Rheinberger", "A trusted subordinate of Erwin Smith."),
    ("Dieter Ness", "A skilled horseman and seasoned Scout Regiment officer."),
    ("Rico Brzenska", "A tough and disciplined squad leader in the Garrison Regiment."),
]

ITEMS_PER_PAGE = 6

# Function to generate the inline keyboard for cadets list
def generate_keyboard(page):
    keyboard = []
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    for i in range(start, min(end, len(cadets)), 2):
        row = [
            InlineKeyboardButton(cadets[i][0], callback_data=f"info_{i}"),
        ]
        if i + 1 < len(cadets):
            row.append(InlineKeyboardButton(cadets[i + 1][0], callback_data=f"info_{i + 1}"))
        keyboard.append(row)

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅ Back", callback_data=f"page_{page - 1}"))
    if end < len(cadets):
        nav_buttons.append(InlineKeyboardButton("Next ➡", callback_data=f"page_{page + 1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton("🏠 Back to Home", callback_data="home")])
    return InlineKeyboardMarkup(keyboard)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = generate_keyboard(0)
    await update.message.reply_text("📜 **Scout Regiment Cadets**:
Choose a cadet to view details.", reply_markup=keyboard)

# Callback handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("page_"):
        page = int(query.data.split("_")[1])
        await query.edit_message_text("📜 **Scout Regiment Cadets**:
Choose a cadet to view details.", reply_markup=generate_keyboard(page))

    elif query.data.startswith("info_"):
        index = int(query.data.split("_")[1])
        name, description = cadets[index]
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("⬅ Back", callback_data="cadet_list")]])
        await query.edit_message_text(f"**{name}**

{description}", reply_markup=keyboard)

    elif query.data == "cadet_list":
        await query.edit_message_text("📜 **Scout Regiment Cadets**:
Choose a cadet to view details.", reply_markup=generate_keyboard(0))

    elif query.data == "home":
        await query.edit_message_text("🏠 **Welcome to the Scout Regiment Bot!**

Use /start to view cadets.")

# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
