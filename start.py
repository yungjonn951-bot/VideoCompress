import os
import sys
import logging
from flask import Flask
from threading import Thread
from pymongo import MongoClient

# --- 1. SETUP LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 2. CRON JOB SERVER (Flask) ---
# This keeps Render from sleeping if you use a pinger like cron-job.org
app = Flask('')

@app.route('/')
def home():
    return "Bot is Online & Database Linked."

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Start the server in the background
Thread(target=run_server, daemon=True).start()

# --- 3. MONGODB CONNECTION ---
MONGO_URL = os.getenv("MONGO_URL")
if MONGO_URL:
    try:
        # Connecting to MongoDB
        client = MongoClient(MONGO_URL)
        client.admin.command('ping') # Test the connection
        logger.info("✅ MongoDB connected successfully!")
    except Exception as e:
        logger.error(f"❌ MongoDB Connection Failed: {e}")

# --- 4. START THE ORIGINAL REPO ---
# This runs the bot logic inside your 'bot' folder
logger.info("--- Launching Main Bot Engine ---")
try:
    import bot.__main__
except Exception as e:
    logger.error(f"❌ Error starting bot logic: {e}")