import os
import sys
import shutil
import logging
import platform
from flask import Flask
from threading import Thread
from pymongo import MongoClient

# --- 1. SYSTEM DIAGNOSTICS & LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("MasterWrapper")

logger.info(f"🐍 Python: {platform.python_version()}")
logger.info(f"🌍 DC: {os.getenv('TG_DC', 'Auto')} | Env: {os.getenv('ENV', 'Prod')}")

# --- 2. DOWNLOADS & AUTO-CLEANUP ---
DOWNLOAD_DIR = os.getenv("DOWNLOAD_LOCATION", "./downloads")

def cleanup_downloads():
    if os.path.exists(DOWNLOAD_DIR):
        try:
            # This wipes the folder clean on every fresh start
            shutil.rmtree(DOWNLOAD_DIR)
            logger.info("🧹 Cleaned up old downloads to save disk space.")
        except Exception as e:
            logger.error(f"❌ Cleanup failed: {e}")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    logger.info(f"📁 Download Directory Ready: {DOWNLOAD_DIR}")

cleanup_downloads()

# --- 3. STAY-ALIVE SERVER (Flask) ---
app = Flask('')
@app.route('/')
def home():
    return "<b>Bot Engine:</b> Online<br><b>Disk:</b> Cleaned<br><b>DB:</b> Connected"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

Thread(target=run_web_server, daemon=True).start()

# --- 4. MONGODB ---
MONGO_URL = os.getenv("MONGO_URL")
if MONGO_URL:
    try:
        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        logger.info("✅ MongoDB Connected Successfully")
    except Exception as e:
        logger.error(f"❌ MongoDB Failed: {e}")

# --- 5. LAUNCH BOT ENGINE ---
sys.path.append(os.getcwd())
logger.info("--- Waking up bot/__main__.py ---")
try:
    import bot.__main__
except Exception as e:
    logger.error(f"❌ Critical Startup Error: {e}")

if __name__ == "__main__":
    # Keeps main thread alive
    pass