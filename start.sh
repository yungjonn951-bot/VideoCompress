#!/bin/bash

# --- 1. PRINT STATUS ---
echo "--- Initializing Environment ---"
python3 --version
ffmpeg -version | head -n 1

# --- 2. START THE BOT ---
# We use 'exec' to make sure Python handles system signals (like shutdowns) correctly
echo "--- Starting Video Compressor Bot ---"
exec python3 start.py
python3 -m bot
