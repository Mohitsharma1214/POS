
from dotenv import load_dotenv
load_dotenv()
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    TWITTER_API_KEY: str = os.getenv("TWITTER_API_KEY", "")

print("[DEBUG] YOUTUBE_API_KEY:", os.getenv("YOUTUBE_API_KEY"))

    class Config:
        env_file = ".env"

settings = Settings()
