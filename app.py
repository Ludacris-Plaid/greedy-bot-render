import os
import logging
from flask import Flask, request, Response
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
logger.info(f"Loaded BOT_TOKEN: {'set' if TOKEN else 'not set'}")

@app.route("/", methods=["GET", "HEAD"])
def health_check():
    logger.info("Received health check request")
    return Response("Bot is running", status=200)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Processing /start command")
    await update.message.reply_text("Hello! I'm Greedy Telegram Bot on Render.")

@app.route("/webhook", methods=["POST"])
async def webhook():
    logger.info("Received webhook request")
    if not TOKEN:
        logger.error("BOT_TOKEN is missing")
        return Response("Missing BOT_TOKEN", status=500)
    try:
        bot = Bot(TOKEN)
        update = Update.de_json(request.get_json(force=True), bot)
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        await application.process_update(update)
        logger.info("Webhook processed successfully")
        return Response(status=200)
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return Response(f"Error: {str(e)}", status=500)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Flask on 0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
