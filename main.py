# -*- coding: utf-8 -*-
from telethon.sessions import StringSession
from telethon import TelegramClient, events
import os
from dotenv import load_dotenv
import asyncio
from threading import Event

# কনফিগ লোড
load_dotenv()

# টেলিথন ক্লায়েন্ট সেটআপ
client = TelegramClient(
    StringSession(os.getenv('SESSION_STRING')),
    int(os.getenv('API_ID')),
    os.getenv('API_HASH')
)

# গ্লোবাল ভেরিয়েবল
is_sending = Event()
current_message = ""
send_interval = 300  # ডিফল্ট ইন্টারভাল 5 মিনিট

@client.on(events.NewMessage(pattern='/start'))
async def handle_start(event):
    if event.sender_id == int(os.getenv('ADMIN_ID')):
        await event.reply('''
        🎛 ইউজারবট কমান্ড:
        /sendall <মেসেজ> - সব গ্রুপে পাঠান
        /stop - বার্তা পাঠানো বন্ধ করুন
        /setinterval <সেকেন্ড> - ইন্টারভাল সেট করুন
        /status - বট স্ট্যাটাস চেক করুন
        ''')

@client.on(events.NewMessage(pattern='/sendall'))
async def handle_send_all(event):
    global current_message, is_sending
    if event.sender_id == int(os.getenv('ADMIN_ID')):
        message = event.raw_text.replace('/sendall', '').strip()
        if message:
            current_message = message
            is_sending.set()
            await event.reply(f"🔃 বার্তা পাঠানো শুরু হয়েছে!\nইন্টারভাল: {send_interval} সেকেন্ড\n/stop দিয়ে বন্ধ করুন")
            await continuous_send()
        else:
            await event.reply("⚡ ব্যবহার: /sendall <মেসেজ>")

@client.on(events.NewMessage(pattern='/stop'))
async def handle_stop(event):
    global is_sending
    if event.sender_id == int(os.getenv('ADMIN_ID')):
        is_sending.clear()
        await event.reply("⛔ বার্তা পাঠানো বন্ধ করা হয়েছে")

@client.on(events.NewMessage(pattern='/setinterval'))
async def handle_set_interval(event):
    global send_interval
    if event.sender_id == int(os.getenv('ADMIN_ID')):
        try:
            interval = int(event.raw_text.split()[1])
            if interval < 60:
                await event.reply("⚠️ ইন্টারভাল কমপক্ষে 60 সেকেন্ড হতে হবে")
                return
            send_interval = interval
            await event.reply(f"🔄 ইন্টারভাল সেট করা হয়েছে: {send_interval} সেকেন্ড")
        except (IndexError, ValueError):
            await event.reply("⚡ ব্যবহার: /setinterval <সেকেন্ড>")

@client.on(events.NewMessage(pattern='/status'))
async def handle_status(event):
    if event.sender_id == int(os.getenv('ADMIN_ID')):
        status = "চালু ✅" if is_sending.is_set() else "বন্ধ ❌"
        await event.reply(f'''
        📊 বট স্ট্যাটাস:
        অবস্থা: {status}
        ইন্টারভাল: {send_interval} সেকেন্ড
        সর্বশেষ বার্তা: {current_message[:50] + '...' if current_message else 'N/A'}
        ''')

async def continuous_send():
    while is_sending.is_set():
        groups = os.getenv('GROUPS').split(',')
        success_count = 0
        
        for group in groups:
            if not is_sending.is_set():
                break
                
            try:
                await client.send_message(int(group), current_message)
                print(f"✅ মেসেজ পাঠানো হয়েছে → {group}")
                success_count += 1
            except Exception as e:
                print(f"❌ গ্রুপ {group} তে ত্রুটি: {e}")
        
        print(f"📊 {success_count}/{len(groups)} গ্রুপে সফলভাবে পাঠানো হয়েছে")
        
        # ইন্টারভাল পর্যন্ত অপেক্ষা করুন
        for _ in range(send_interval):
            if not is_sending.is_set():
                break
            await asyncio.sleep(1)

async def main():
    await client.start()
    print("🔹 ইউজারবট সক্রিয় হয়েছে...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())            await update.message.reply_text("❌ Links are not allowed!")
        except Exception as e:
            logger.warning(f"Error deleting message: {e}")

async def add_no_exempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usage: /addnoexempt <group_id> <user_id>")
        return
    try:
        chat_id = int(context.args[0])
        user_id = int(context.args[1])

        if chat_id not in group_no_exempt_admin_ids:
            group_no_exempt_admin_ids[chat_id] = []

        if user_id not in group_no_exempt_admin_ids[chat_id]:
            group_no_exempt_admin_ids[chat_id].append(user_id)
            await update.message.reply_text(f"✅ User ID {user_id} added to no-exempt list for group {chat_id}.")
        else:
            await update.message.reply_text(f"ℹ️ User ID {user_id} already in no-exempt list for group {chat_id}.")
    except ValueError:
        await update.message.reply_text("❌ Invalid IDs.")

async def remove_no_exempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Usage: /removenoexempt <group_id> <user_id>")
        return
    try:
        chat_id = int(context.args[0])
        user_id = int(context.args[1])

        if chat_id in group_no_exempt_admin_ids and user_id in group_no_exempt_admin_ids[chat_id]:
            group_no_exempt_admin_ids[chat_id].remove(user_id)
            await update.message.reply_text(f"✅ User ID {user_id} removed from no-exempt list for group {chat_id}.")
        else:
            await update.message.reply_text(f"ℹ️ User ID {user_id} not found in no-exempt list for group {chat_id}.")
    except ValueError:
        await update.message.reply_text("❌ Invalid IDs.")

async def list_no_exempt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("⚠️ Usage: /listnoexempt <group_id>")
        return
    try:
        chat_id = int(context.args[0])
        if chat_id not in group_no_exempt_admin_ids or not group_no_exempt_admin_ids[chat_id]:
            await update.message.reply_text(f"ℹ️ No user IDs in no-exempt list for group {chat_id}.")
        else:
            ids_text = "\n".join(str(uid) for uid in group_no_exempt_admin_ids[chat_id])
            await update.message.reply_text(f"📝 No-exempt list for group {chat_id}:\n{ids_text}")
    except ValueError:
        await update.message.reply_text("❌ Invalid group ID.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running and ready!\nYou can control me via private chat using group IDs.")

app = ApplicationBuilder().token(TOKEN).build()

# Command handlers
app.add_handler(CommandHandler("addnoexempt", add_no_exempt))
app.add_handler(CommandHandler("removenoexempt", remove_no_exempt))
app.add_handler(CommandHandler("listnoexempt", list_no_exempt))
app.add_handler(CommandHandler("start", start))

# Message handler for links
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), delete_links))

logger.info("✅ Bot is running...")
app.run_polling()
