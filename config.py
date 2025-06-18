from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MOCK_CAMERA_PATH = BASE_DIR / "mock_camera" / "DCIM" / "100CANON"
DEST_ROOT = BASE_DIR / "output"
LOG_FILE = BASE_DIR / "transfer_log.txt"

# Заглушка для Telegram
TELEGRAM_ENABLED = True  # Включить True для реальной отправки
BOT_TOKEN = "7611900550:AAFXp25fSsgy5COOMWFWcppyWYjGXXprIrs"