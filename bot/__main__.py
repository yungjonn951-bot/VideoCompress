import os
import logging
from pyrogram import Client, idle
from bot.config import Config

# --- 1. SETUP LOGGING ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 2. INITIALIZE CLIENT ---
# in_memory=True prevents session corruption on Render's temporary disk
app = Client(
    "VideoCompressorBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="bot/plugins"), 
    in_memory=True
)

async def run_bot():
    try:
        await app.start()
        
        # --- 3. THE RECOVERY STEP ---
        # Clears pending messages sent while the bot was offline 
        # to prevent it from getting stuck in an error loop.
        await app.get_updates(offset=-1)
        
        me = await app.get_me()
        logger.info(f"✅ Bot is Online: @{me.username}")
        
        # Keep the bot alive
        await idle()
        
    except Exception as e:
        logger.error(f"❌ Startup Error: {e}")
    finally:
        await app.stop()

if __name__ == "__main__":
    # This runs the bot and ensures it doesn't get blocked by the web server
    app.run(run_bot())