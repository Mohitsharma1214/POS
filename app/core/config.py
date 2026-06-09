from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ANTHROPIC_API_KEY: str = ""
    TAVILY_API_KEY: str = ""
    APIFY_API_TOKEN: str = ""
    

    MODEL_HAIKU: str = "claude-haiku-4-5-20251001"
    MODEL_SONNET: str = "claude-sonnet-4-6"
    MODEL_OPUS: str = "claude-opus-4-6"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
