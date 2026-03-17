import os
import sys
import logging
import platform
from flask import Flask
from threading import Thread
from pymongo import MongoClient

# --- 1. SYSTEM DIAGNOSTICS ---
# This prints your setup details to the Render logs for easy monitoring.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SystemCheck")

logger.info(f"🐍 Python Version: {platform.python_version()}")
logger.info(f"🌍 Telegram DC: {os.getenv('TG_DC', 'Auto-Detect')}")
logger.info(f"🛠️ Environment: {os.getenv('ENV', 'Production')}")
logger.info(f"📡 Port: {os.getenv('PORT', '8080')}")

# --- 2. CRON-JOB / STAY-ALIVE SERVER (Flask) ---
app = Flask('')

@app.route('/')
def home():
    return "<b>Bot Status:</b> Operational<br><b>Database:</b> Linked<br><b>Stay-Alive:</b> Active"

def run_server():
    # Render's dynamic port
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Start the Flask server in a separate thread so it doesn't block the bot
Thread(target=run_server, daemon=True).start()

# --- 3. MONGODB CONNECTION ---
MONGO_URL = os.getenv("MONGO_URL")
if MONGO_URL:
    try:
        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        logger.info("✅ MongoDB: Connected Successfully")
    except Exception as e:
        logger.error(f"❌ MongoDB: Connection Failed ({e})")
else:
    logger.warning("⚠️ MONGO_URL not found. Database features may be limited.")

# --- 4. START THE BOT ENGINE ---
# This reaches into your /bot folder and triggers the entire modular logic.
sys.path.append(os.getcwd())
logger.info("--- Waking up the Bot Engine from /bot/__main__.py ---")

try:
    import bot.__main__
except Exception as e:
    logger.error(f"❌ Critical error launching bot: {e}")

if __name__ == "__main__":
    # Keep the main thread alive while the background threads run
    pass