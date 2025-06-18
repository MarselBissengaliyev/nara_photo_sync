import json
import asyncio
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# Настройка логирования
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
            data = json.load(f)
            logger.info(f"Загружено {len(data)} подписчиков.")
            return set(data)
    except FileNotFoundError:
        logger.warning(f"Файл {SUBSCRIBERS_FILE} не найден, создается новый.")
        return set()
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка разбора JSON: {e}")
        return set()
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при загрузке chat_ids: {e}")
        return set()


def save_chat_ids(ids: set[int]):
    try:
        with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
            json.dump(list(ids), f, ensure_ascii=False, indent=2)
        logger.info(f"Сохранено {len(ids)} подписчиков.")
    except Exception as e:
        logger.exception(f"Ошибка при сохранении chat_ids: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.effective_chat is None:
            logger.warning("update.effective_chat отсутствует.")
            return

        chat_id = update.effective_chat.id
        subscribers = load_chat_ids()

        if chat_id in subscribers:
            text = "🔔 Вы уже подписаны на уведомления."
        else:
            subscribers.add(chat_id)
            save_chat_ids(subscribers)
            text = "✅ Вы подписаны на уведомления!"

        await context.bot.send_message(chat_id=chat_id, text=text)

    except Exception as e:
        logger.exception(f"Ошибка в обработчике /start: {e}")


def main():
    try:
        application = Application.builder().token(TOKEN).build()

        application.add_handler(CommandHandler("start", start))

        logger.info("🤖 Бот запущен. Ожидает команду /start...")
        application.run_polling()
    except Exception as e:
        logger.exception(f"Ошибка при запуске бота: {e}")


if __name__ == "__main__":
    main()
