import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8913640033:AAGEzpXTxVmFX-vuR4TNW9ZjXusUKsfim5U"
URL = "https://YOUR-RAILWAY-APP.up.railway.app"  # потом заменишь

START_COUNT = 10
dinners = {}

app_flask = Flask(__name__)
bot_app = Application.builder().token(TOKEN).build()


# ---------- КЛАВИАТУРА ----------
def get_keyboard(count: int):
    buttons = []

    if count > 0:
        buttons.append([
            InlineKeyboardButton("🍽 Заказать минт", callback_data="order")
        ])

    buttons.append([
        InlineKeyboardButton("🍷 Заказать дополнительные услуги", callback_data="buy_more")
    ])

    return InlineKeyboardMarkup(buttons)


# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    dinners[chat_id] = START_COUNT

    text = (
        "🫶С днём рождения, моя нежная Любовь!\n"
        "Спасибо что есть в моей жизни.\n"
        "Хоть ты и не мой, но мне легче жить в этом мире, зная, что где-то ты рядом.\n"
        "Очень ценю и уважаю тебя, мой Воин 🐺🐅🦁\n\n"
        " "
        "🎉 Вам подарено 10 минтов 🍽"
        "для заказа нажмите на кнопку ниже,"
        "а потоп отправьте скоин исполнителю для бронирования даты"
     
    )

    await update.message.reply_text(text, reply_markup=get_keyboard(START_COUNT))


# ---------- CALLBACK ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    data = query.data

    count = dinners.get(chat_id, START_COUNT)

    # заказ минта
    if data == "order":
        if count <= 0:
            await query.message.reply_text("У вас больше не осталось минтов 😢")
            return

        count -= 1
        dinners[chat_id] = count

        await query.message.reply_text("🍽 Минт заказан!")

        if count > 0:
            await query.message.reply_text(f"Осталось минтов: {count}")
        else:
            await query.message.reply_text(
                "У вас закончились все минты 🎉\n\n"
                "Нажмите кнопку ниже 👇",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🍷 Заказать дополнительные услуги", callback_data="buy_more")
                ]])
            )

    # купить
    elif data == "buy_more":
        await query.message.reply_text(
            "🍷 Конечно можем договориться.\n"
            "Напишите нам, и мы обсудим детали 😉"
        )


# ---------- WEBHOOK ----------
@app_flask.route(f"/webhook/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json()
    update = Update.de_json(data, bot_app)

    await bot_app.process_update(update)
    return "ok"


# ---------- SET WEBHOOK ----------
@app_flask.route("/set_webhook")
def set_webhook():
    url = f"{URL}/webhook/{TOKEN}"
    bot_app.bot.set_webhook(url=url)
    return f"Webhook set to {url}"


# ---------- START BOT HANDLERS ----------
bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(CallbackQueryHandler(button_handler))


# ---------- RUN ----------
if __name__ == "__main__":
    app_flask.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
