from telegram import Update, InputMediaPhoto, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
import json
import os
from datetime import datetime

ADMIN_ID = 7734095649  # ✅ নিজের আইডি বসাও
USER_FILE = "data/users.json"
CONFIG_FILE = "data/config.json"  # 🆕 নতুন যোগ

def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

# 🆕 মেনু কনফিগ লোডার
def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"menus": []}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

# 🆕 ডাইনামিক বাটন জেনারেটর
def get_dynamic_buttons():
    config = load_config()
    buttons = [[btn["name"]] for btn in config.get("menus", [])]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# ✅ START হ্যান্ডলার
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users = load_users()

    if str(user.id) not in users:
        users[str(user.id)] = {
            "name": user.full_name,
            "username": user.username,
            "join_date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "banned": False
        }
        save_users(users)

        # 📨 অ্যাডমিনকে মেসেজ
        total_users = len(users)
        msg = (
            "🆕 <b>New User Joined</b>\n"
            f"👤 Name: {user.full_name}\n"
            f"🔗 Username: @{user.username or 'N/A'}\n"
            f"📅 Join Date: {users[str(user.id)]['join_date']}\n"
            f"👥 Total Users: {total_users}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="HTML")

    # 📸 ছবি ও মেসেজ
    await update.message.reply_photo(
        photo="https://i.postimg.cc/0yCpmF6B/1751575789815.jpg",
        caption="🌀 <b>Wellcome To MaxtonXBot</b>",
        parse_mode="HTML"
    )

    # 🆕 ডাইনামিক মেনু বাটন দেখাও
    await update.message.reply_text(
        "👇 Choose an option:",
        reply_markup=get_dynamic_buttons()
    )

start_handler = CommandHandler("start", start)
