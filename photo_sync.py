from config import (
    MOCK_CAMERA_PATH,
    DEST_ROOT,
    LOG_FILE,
    TELEGRAM_ENABLED,
    BOT_TOKEN,
)
from pathlib import Path
import shutil
from datetime import datetime
import logging
import requests
import json
import traceback

PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".JPG", ".JPEG"}

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def is_new_file(file_path: Path, target_folder: Path) -> bool:
    return not (target_folder / file_path.name).exists()


def notify_telegram(message: str):
    if not TELEGRAM_ENABLED:
        logger.info(f"[TELEGRAM ЗАГЛУШКА] {message}")
        return

    try:
        with open("subscribers.json", "r") as f:
            chat_ids = json.load(f)
    except Exception as e:
        logger.error(f"Не удалось загрузить chat_ids: {e}")
        return

    for chat_id in chat_ids:
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": chat_id, "text": message},
                timeout=10
            )
            if response.status_code != 200:
                logger.warning(f"Ошибка отправки в Telegram: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"Telegram error: {e}")


def copy_new_photos():
    try:
        if not MOCK_CAMERA_PATH.exists():
            msg = "❌ Мок-папка камеры не найдена."
            logger.error(msg)
            print(msg)
            return

        folder_name = datetime.now().strftime("%d%m%y_%H%M")
        dest_folder = DEST_ROOT / folder_name
        try:
            dest_folder.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Не удалось создать папку {dest_folder}: {e}")
            return

        copied_files = []

        for photo in MOCK_CAMERA_PATH.iterdir():
            try:
                if photo.suffix in PHOTO_EXTENSIONS and photo.is_file():
                    if is_new_file(photo, dest_folder):
                        shutil.copy(photo, dest_folder / photo.name)
                        copied_files.append(photo.name)
                        logger.info(f"Скопирован файл: {photo.name}")
            except Exception as e:
                logger.error(f"Ошибка при копировании {photo.name}: {e}")
                logger.debug(traceback.format_exc())

        if copied_files:
            msg = f"✅ Скопировано файлов: {len(copied_files)}"
            logger.info(f"Скопированы фото: {copied_files}")
            print(msg)
            notify_telegram(msg)
        else:
            msg = "ℹ️ Новых файлов для копирования не найдено."
            logger.info(msg)
            print(msg)
            notify_telegram(msg)

    except Exception as e:
        logger.critical(f"Необработанная ошибка в copy_new_photos: {e}")
        logger.debug(traceback.format_exc())
        print(f"❌ Критическая ошибка: {e}")


if __name__ == "__main__":
    logger.info("📷 Запуск скрипта копирования фотографий")
    copy_new_photos()
