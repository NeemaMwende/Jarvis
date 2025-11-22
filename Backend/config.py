import os
from dotenv import load_dotenv

load_dotenv()

WAKE_WORD = "jarvis"
USE_OFFLINE_STT = True
USE_OFFLINE_TTS = False
MODEL_NAME = "qwen3:1.7b"
DATA_DIR = os.path.join(os.getcwd(), "data")
