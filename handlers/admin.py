from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes,
    ConversationHandler, filters
)
import json
import os

# 🔧 ফাইল লোকেশন
CONFIG_FILE = "data/config.json"
USER_FILE = "data/users.json"
BANNED_FILE = "data/banned.json"

# 📦 JSON লোড ও সেভ ফাংশন
def load_json(path):
    if not os.path.exists(path):
        return {} if "config" in path else []
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ✅ /admin কমান্ড - এডমিন প্যানেল দেখানো
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    config = load_json(CONFIG_FILE)

    if user_id not in config.get("admins", []):
        return await update.message.reply_text("❌ You are not authorized.")

    keyboard = [
        [InlineKeyboardButton("➕ Add Menu", callback_data="add_menu")],
        [InlineKeyboardButton("📂 View Menus", callback_data="view_menus")],
        [InlineKeyboardButton("📢 Message All", callback_data="message_all")],
        [InlineKeyboardButton("📊 Statistics", callback_data="stats")],
        [InlineKeyboardButton("🚫 Ban / ✅ Unban", callback_data="ban_unban")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("🔐 Welcome to Admin Panel", reply_markup=reply_markup)

# ✅ Message All সিস্টেম
ASK_BROADCAST = range(1)

async def message_all_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📨 Send the message you want to broadcast to all users:")
    return ASK_BROADCAST

async def broadcast_to_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return await update.message.reply_text("❗ Please send text only.")
    
    users = load_json(USER_FILE)

    success = 0
    fail = 0

    for user_id in users:
        if users[user_id].get("banned", False):
            continue
        try:
            await context.bot.send_message(chat_id=int(user_id), text=text)
            success += 1
        except:
            fail += 1

    await update.message.reply_text(f"✅ Message sent to {success} users.\n❌ Failed to send to {fail} users.")
    return ConversationHandler.END

# ✅ হ্যান্ডলার লিস্ট
admin_handlers = [
    CommandHandler("admin", admin_panel),
    CallbackQueryHandler(message_all_prompt, pattern="^message_all$"),
    ConversationHandler(
        entry_points=[CallbackQueryHandler(message_all_prompt, pattern="^message_all$")],
        states={
            ASK_BROADCAST: [MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_to_all)]
        },
        fallbacks=[],
    )
]
