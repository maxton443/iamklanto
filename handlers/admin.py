from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
import json
import os

CONFIG_FILE = "data/config.json"
USER_FILE = "data/users.json"
BANNED_FILE = "data/banned.json"

def load_json(path):
    if not os.path.exists(path):
        return {} if "config" in path else []
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ✅ /admin কমান্ড
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    config = load_json(CONFIG_FILE)

    if user_id not in config["admins"]:
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

admin_handlers = [
    CommandHandler("admin", admin_panel)
]

# এখানে আমরা পরের ধাপে add_menu, view_menus, message_all ইত্যাদির জন্য CallbackQueryHandler যোগ করব।
