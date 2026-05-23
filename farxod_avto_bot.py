import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8609836492:AAGGWYdJQpSZH6K9YfC-akyAttZLjJkca78"

ADMIN_USERNAMES = ["sardorbek_admin", "Jamol_admin", "beknur_admin"]
ADMIN_IDS = []

logging.basicConfig(level=logging.INFO)

async def forward_to_admins(context, user, message_text):
    text = (
        f"📩 Yangi xabar!\n\n"
        f"👤 Foydalanuvchi: {user.full_name}\n"
        f"🔗 Username: @{user.username if user.username else 'Yoq'}\n"
        f"🆔 ID: {user.id}\n\n"
        f"💬 Xabar:\n{message_text}"
    )
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=text)
        except:
            pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username in ADMIN_USERNAMES and user.id not in ADMIN_IDS:
        ADMIN_IDS.append(user.id)

    keyboard = [
        [InlineKeyboardButton("📍 Manzil", callback_data="manzil")],
        [InlineKeyboardButton("📞 Telefon raqamlar", callback_data="telefon")],
        [InlineKeyboardButton("🕐 Ish vaqti", callback_data="ish_vaqti")],
        [InlineKeyboardButton("💬 Admin bilan bog'lanish", callback_data="admin")],
    ]
    await update.message.reply_text(
        "🚗 *Farxod Avto*ga xush kelibsiz!\n\nQuyidagilardan birini tanlang:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "manzil":
        keyboard = [[InlineKeyboardButton("🗺️ Google Maps da ochish", url="https://maps.app.goo.gl/APGc3N1g47hRN2kv5")]]
        await query.edit_message_text(
            "📍 *Manzilimiz:*\n\nBuxoro viloyat, Vobkent tuman\n\nPastdagi tugmani bosib yo'nalish oling 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard + [[InlineKeyboardButton("🔙 Orqaga", callback_data="back")]])
        )
    elif query.data == "telefon":
        await query.edit_message_text(
            "📞 *Telefon raqamlarimiz:*\n\n📱 +998 94 129 77 66\n📱 +998 77 777 69 92\n📱 +998 93 744 77 66",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data="back")]])
        )
    elif query.data == "ish_vaqti":
        await query.edit_message_text(
            "🕐 *Ish vaqtimiz:*\n\n⏰ Har kuni: 08:30 — 18:00\n\nSizni kutamiz! 🚗",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data="back")]])
        )
    elif query.data == "admin":
        context.user_data["waiting_message"] = True
        await query.edit_message_text(
            "💬 *Admin bilan bog'lanish:*\n\nXabaringizni yozing, adminlarimiz tez orada javob beradi! 👇",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data="back")]])
        )
    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("📍 Manzil", callback_data="manzil")],
            [InlineKeyboardButton("📞 Telefon raqamlar", callback_data="telefon")],
            [InlineKeyboardButton("🕐 Ish vaqti", callback_data="ish_vaqti")],
            [InlineKeyboardButton("💬 Admin bilan bog'lanish", callback_data="admin")],
        ]
        await query.edit_message_text(
            "🚗 *Farxod Avto*\n\nQuyidagilardan birini tanlang:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.username in ADMIN_USERNAMES and user.id not in ADMIN_IDS:
        ADMIN_IDS.append(user.id)

    if context.user_data.get("waiting_message"):
        context.user_data["waiting_message"] = False
        await forward_to_admins(context, user, update.message.text)
        await update.message.reply_text("✅ Xabaringiz adminlarga yuborildi!\nTez orada bog'lanamiz. 🚗")
        keyboard = [
            [InlineKeyboardButton("📍 Manzil", callback_data="manzil")],
            [InlineKeyboardButton("📞 Telefon raqamlar", callback_data="telefon")],
            [InlineKeyboardButton("🕐 Ish vaqti", callback_data="ish_vaqti")],
            [InlineKeyboardButton("💬 Admin bilan bog'lanish", callback_data="admin")],
        ]
        await update.message.reply_text(
            "🚗 *Farxod Avto*\n\nBoshqa savollaringiz bo'lsa:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text("Iltimos /start tugmasini bosing.")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("Bot ishlamoqda...")
    app.run_polling()
