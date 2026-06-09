import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class YouTubeKeyManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(YouTubeKeyManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        keys_str = os.getenv("YOUTUBE_API_KEY", "")
        self.keys = [k.strip() for k in keys_str.split(",") if k.strip()]
        self.current_index = 0
        
        if not self.keys:
            logger.warning("No YOUTUBE_API_KEY found in environment.")
        else:
            logger.info(f"Initialized YouTubeKeyManager with {len(self.keys)} API keys.")

    def get_current_key(self) -> Optional[str]:
        if not self.keys:
            return None
        return self.keys[self.current_index]

    def mark_key_exhausted(self):
        if not self.keys:
            return
        
        old_index = self.current_index
        self.current_index = (self.current_index + 1) % len(self.keys)
        logger.warning(f"YouTube API Key at index {old_index} exhausted (403/Quota Exceeded). Switched to key index {self.current_index}.")

    def has_keys(self) -> bool:
        return len(self.keys) > 0
