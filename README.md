from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MOCK_CAMERA_PATH = BASE_DIR / "mock_camera" / "DCIM" / "100CANON"
DEST_ROOT = BASE_DIR / "output"
LOG_FILE = BASE_DIR / "transfer_log.txt"

# Заглушка для Telegram
TELEGRAM_ENABLED = False  # Включить True для реальной отправки
BOT_TOKEN = "your_bot_token"
CHAT_IDS = ["chat_id_1", "chat_id_2"]
