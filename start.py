import os
import sys
import logging
from flask import Flask
from threading import Thread
from pymongo import MongoClient

# --- 1. SYSTEM SETUP ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Wrapper")

# Add current directory to path so the 'bot' package is found
sys.path.append(os.getcwd())

# --- 2. CRON JOB SERVER (Stay-Alive) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Engine: ACTIVE<br>Cron Job Status: RECEIVING"

def run_server():
    # Render uses the PORT env var; defaults to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Run the server in a separate thread
Thread(target=run_server, daemon=True).start()

# --- 3. MONGODB ---
# This ensures MongoDB is ready before the bot starts
MONGO_URL = os.getenv("MONGO_URL")
if MONGO_URL:
    try:
        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        logger.info("✅ MongoDB connected successfully.")
    except Exception as e:
        logger.error(f"❌ MongoDB failed: {e}")
else:
    logger.warning("⚠️ No MONGO_URL found in environment variables.")

# --- 4. START THE BOT ENGINE ---
# This triggers the original __main__.py inside your /bot folder
logger.info("--- Waking up the Bot Engine ---")
try:
    import bot.__main__
except Exception as e:
    logger.error(f"❌ Critical error launching bot: {e}")

if __name__ == "__main__":
    # Keep the script running
    pass
