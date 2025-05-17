# config/settings.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

class Settings:
    EXATI_URL = os.getenv("EXATI_URL", "https://exati.com.br")
    MODEL_PATH = BASE_DIR / "assets/models/led_classifier.h5"
    SCREENSHOT_DIR = BASE_DIR / "assets/screenshots"

settings = Settings()