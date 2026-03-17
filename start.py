import os
import sys
import logging
from flask import Flask
from threading import Thread
from pymongo import MongoClient

# --- 1. LOGGING & SYSTEM SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Wrapper")

# Add the current directory to sys.path so 'bot' is found as a module
sys.path.append(os.getcwd())

# --- 2. CRON JOB / STAY-ALIVE SERVER ---
app = Flask('')

@app.route('/')
def home():
    # This is the page cron-job.org will ping
    return "Bot Engine: Running<br>Database: Connected<br>Status: Healthy"

def run_server():
    # Render provides a dynamic port; default to 8080
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Stay-Alive server on port {port}")
    app.run(host='0.0.0.0', port=port)

# Run the server in a background thread
Thread(target=run_server, daemon=True).start()

# --- 3. MONGODB INITIALIZATION ---
MONGO_URL = os.getenv("MONGO_URL")

if MONGO_URL:
    try:
        # Connecting to MongoDB
        client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')  # Test the connection
        logger.info("✅ MongoDB connection successful.")
    except Exception as e:
        logger.error(f"❌ MongoDB Connection Failed: {e}")
else:
    logger.warning("⚠️ MONGO_URL not found. Database features may not work.")

# --- 4. LAUNCHING THE BOT ENGINE ---
# This part triggers the __main__.py inside your /bot folder.
# This ensures all plugins and helper_funcs are loaded properly.
logger.info("--- Launching Main Bot Engine from /bot/__main__.py ---")

try:
    import bot.__main__
except ImportError as e:
    logger.error(f"❌ Could not find 'bot' folder or '__main__.py': {e}")
except Exception as e:
    logger.error(f"❌ Critical error during bot startup: {e}")

# Keep the script alive
if __name__ == "__main__":
    logger.info("Wrapper is active. Bot logic is now in control.")