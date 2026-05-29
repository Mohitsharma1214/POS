from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APIFY_API_TOKEN: str = ""
    TWITTER_API_KEY: str = ""
    X_USERNAME: str = ""
    X_EMAIL: str = ""
    X_PASSWORD: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()
