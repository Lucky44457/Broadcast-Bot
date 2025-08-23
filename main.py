from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, ADMINS
import os

app = Client("blue_backup_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# /start command
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = str(message.from_user.id)

    # Save user if not already in users.txt
    if not os.path.exists("users.txt"):
        open("users.txt", "w").close()

    with open("users.txt", "r") as f:
        users = f.read().splitlines()

    if user_id not in users:
        with open("users.txt", "a") as f:
            f.write(f"{user_id}\n")

    await message.reply_text(
        "🤖 Welcome to Blue Power Backup Bot! 🔋💙\n"
        "🚫 Don't delete or block this bot.\n"
        "📣 After a channel ban, you'll get the updated link here! 🔄\n"
        "🙏 Thanks for staying connected! 💪✨\n\n"
        "🔗 [Join Backup Channel](https://t.me/RulerRock)",
        disable_web_page_preview=True
    )

# /support command
@app.on_message(filters.command("support") & filters.private)
async def support(client, message):
    await message.reply("📞 Our support will reply here as soon as possible.")

# /broadcast command (only for admins)
@app.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast(client, message):
    if not message.reply_to_message:
        await message.reply("⚠️ Reply to a message with /broadcast to send it to all users.")
        return

    try:
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
    except FileNotFoundError:
        await message.reply("❌ No users to broadcast to.")
        return

    sent, failed = 0, 0
    for user_id in users:
        try:
            await message.reply_to_message.copy(chat_id=int(user_id))
            sent += 1
        except:
            failed += 1

    await message.reply(f"✅ Broadcast completed.\n\n📬 Sent: `{sent}`\n❌ Failed: `{failed}`")

# /stats command (only for admins)
@app.on_message(filters.command("stats") & filters.user(ADMINS))
async def stats(client, message):
    try:
        with open("users.txt", "r") as f:
            total_users = len(f.read().splitlines())
    except FileNotFoundError:
        total_users = 0
    await message.reply(f"📊 Total users: {total_users}")

# /reply command (admins reply to users)
@app.on_message(filters.command("reply") & filters.user(ADMINS))
async def reply_user(client, message):
    if len(message.command) < 3:
        await message.reply("⚠️ Usage: `/reply user_id message`", quote=True)
        return

    try:
        user_id = int(message.command[1])
        reply_text = " ".join(message.command[2:])
        await client.send_message(chat_id=user_id, text=reply_text)
        await message.reply("✅ Message sent.")
    except Exception as e:
        await message.reply(f"❌ Failed to send message.\n\nError: {e}")

# /get_users command (only for admins)
@app.on_message(filters.command("get_users") & filters.user(ADMINS))
async def get_users(client, message):
    try:
        if os.path.exists("users.txt") and os.path.getsize("users.txt") > 0:
            await message.reply_document("users.txt")
        else:
            await message.reply("⚠️ No users found or file is empty.")
    except Exception as e:
        await message.reply(f"❌ Error while sending file: {e}")

# Forward user messages to all admins (excluding commands)
@app.on_message(filters.private & ~filters.command(
    ["start", "support", "broadcast", "stats", "reply", "get_users"]
))
async def forward_to_admins(client: Client, message: Message):
    user = message.from_user
    user_info = f"👤 From [{user.first_name}](tg://user?id={user.id}) (`{user.id}`):"
    try:
        for admin_id in ADMINS:
            await client.send_message(
                chat_id=admin_id,
                text=f"{user_info}\n\n{message.text}"
            )
    except Exception as e:
        print(f"Failed to forward message to admins: {e}")

app.run()
