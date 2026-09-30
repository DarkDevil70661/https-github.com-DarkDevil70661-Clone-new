# ShrutixMusic/core/dir.py

import os
from ShrutixMusic.logging import LOGGER

# create logger instance
log = LOGGER("ShrutixMusic")

# Base directories
BASE_DIR = os.getcwd()
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
COUPLE_DIR = os.path.join(BASE_DIR, "couples")
CACHE_DIR = os.path.join(BASE_DIR, "cache")


def dirr():
    """Clean current folder images and ensure required directories exist."""

    # Delete images in current working directory
    for file in os.listdir(BASE_DIR):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            try:
                os.remove(os.path.join(BASE_DIR, file))
            except Exception as e:
                log.warning(f"Failed to remove {file}: {e}")

    # Ensure directories exist
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(COUPLE_DIR, exist_ok=True)

    log.info("Directories updated successfully.")
