import os
from flask import Flask, request, Response
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm Greedy Telegram Bot on Render.")

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
async def webhook():
    if not TOKEN:
        return Response("Missing BOT_TOKEN", status=500)
    bot = Bot(TOKEN)
    update = Update.de_json(request.get_json(force=True), bot)
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    await application.process_update(update)
    return Response(status=200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
