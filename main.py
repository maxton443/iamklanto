from telegram.ext import ApplicationBuilder
from handlers.start import start_handler
from handlers.admin import admin_handlers
from handlers.menu import menu_handlers

app = ApplicationBuilder().token("8058867589:AAEehMvbR4lX9ss_X03gpGuLHFn-UxdbP00").build()

# ✅ হ্যান্ডলার যোগ করা
app.add_handler(start_handler)
app.add_handlers(admin_handlers)
app.add_handlers(menu_handlers)

print("🤖 MaxtonXBot is running...")
app.run_polling()
