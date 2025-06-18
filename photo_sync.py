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

PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".JPG", ".JPEG"}

logging.basicConfig(
    filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s"
)


def is_new_file(file_path: Path, target_folder: Path) -> bool:
    return not (target_folder / file_path.name).exists()


def notify_telegram(message: str):
    if not TELEGRAM_ENABLED:
        print(f"[TELEGRAM ЗАГЛУШКА] {message}")
        return

    try:
        with open("subscribers.json", "r") as f:
            chat_ids = json.load(f)
    except Exception as e:
        print(f"❌ Не удалось загрузить chat_ids: {e}")
        return

    for chat_id in chat_ids:
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data={"chat_id": chat_id, "text": message},
            )
            if response.status_code != 200:
                print(f"⚠️ Ошибка отправки в Telegram: {response.text}")
        except Exception as e:
            print(f"❌ Telegram error: {e}")



def copy_new_photos():
    if not MOCK_CAMERA_PATH.exists():
        print("❌ Мок-папка камеры не найдена.")
        return

    folder_name = datetime.now().strftime("%d%m%y_%H%M")
    dest_folder = DEST_ROOT / folder_name
    dest_folder.mkdir(parents=True, exist_ok=True)

    copied_files = []

    for photo in MOCK_CAMERA_PATH.iterdir():
        if photo.suffix in PHOTO_EXTENSIONS and photo.is_file():
            if is_new_file(photo, dest_folder):
                shutil.copy(photo, dest_folder / photo.name)
                copied_files.append(photo.name)

    if copied_files:
        msg = f"✅ Скопировано файлов: {len(copied_files)}"
        print(msg)
        logging.info(f"Скопированы фото: {copied_files}")
        notify_telegram(msg)
    else:
        msg = "ℹ️ Новых файлов для копирования не найдено."
        print(msg)
        logging.info(msg)
        notify_telegram(msg)


if __name__ == "__main__":
    copy_new_photos()
