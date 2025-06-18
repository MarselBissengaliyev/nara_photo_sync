import json
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7611900550:AAFXp25fSsgy5COOMWFWcppyWYjGXXprIrs"
SUBSCRIBERS_FILE = "subscribers.json"


def load_chat_ids() -> set[int]:
    try:
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()


def save_chat_ids(ids: set[int]):
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(ids), f, ensure_ascii=False, indent=2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if not chat:
        return

    chat_id = chat.id
    subscribers = load_chat_ids()

    if chat_id in subscribers:
        text = "🔔 Вы уже подписаны на уведомления."
    else:
        subscribers.add(chat_id)
        save_chat_ids(subscribers)
        text = "✅ Вы подписаны на уведомления!"

    await context.bot.send_message(chat_id=chat_id, text=text)


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    logger.info("🤖 Бот запущен.")
    application.run_polling()


if __name__ == "__main__":
    main()
