#!/bin/bash

# --- 1. PRINT STATUS ---
echo "--- Initializing Environment ---"
python3 --version
ffmpeg -version | head -n 1

# --- 2. START THE WRAPPER ---
# We run start.py because it contains your MongoDB and Cron Job logic.
# start.py will then automatically trigger the internal 'bot' logic.
echo "--- Starting Wrapper with MongoDB & Cron Job ---"
exec python3 start.py