from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackQueryHandler, MessageHandler, ContextTypes, filters
import json
import os

CONFIG_FILE = "data/config.json"
pending_add = {}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"menus": []}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ✅ Add Menu Handler
async def add_menu_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📝 Send the name for the new menu button:", reply_markup=ReplyKeyboardRemove())
    pending_add[query.from_user.id] = "waiting_for_menu_name"

async def handle_menu_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in pending_add and pending_add[user_id] == "waiting_for_menu_name":
        name = update.message.text
        pending_add[user_id] = {"name": name}
        await update.message.reply_text(f"✅ Menu name set: {name}\n\n📩 Now send the message/content to attach.")
    elif user_id in pending_add and isinstance(pending_add[user_id], dict):
        menu = pending_add[user_id]
        menu["content"] = update.message.text
        config = load_config()
        config["menus"].append(menu)
        save_config(config)
        await update.message.reply_text(f"🎉 Menu '{menu['name']}' added!")
        del pending_add[user_id]

menu_handlers = [
    CallbackQueryHandler(add_menu_prompt, pattern="^add_menu$"),
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_name)
]
