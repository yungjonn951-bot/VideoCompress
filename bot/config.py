import os
import logging
from pyrogram import Client, idle
from bot.config import Config

# --- 1. SETUP LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- 2. INITIALIZE THE CLIENT ---
# We use in_memory=True to avoid disk permission errors on Render
app = Client(
    "VideoCompressorBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.TG_BOT_TOKEN,
    plugins=dict(root="bot/plugins"),
    in_memory=True 
)

async def start_bot():
    try:
        logger.info("🚀 Attempting to start the bot...")
        await app.start()
        
        # This clears old messages so the bot doesn't crash on backlogs
        await app.get_updates(offset=-1)
        
        me = await app.get_me()
        logger.info(f"✅ Bot is Online: @{me.username}")
        
        # This keeps the bot running until you manually stop it
        await idle()
        
    except Exception as e:
        logger.error(f"❌ Critical Startup Error: {e}")
    finally:
        await app.stop()
        logger.info("🛑 Bot has stopped.")

if __name__ == "__main__":
    # This runs the main function
    app.run(start_bot())