from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "bookmarks-api"
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "bookmarksdb"
    mongo_collection: str = "bookmarks"
    api_prefix: str = "/api/v1"
    host: str = "127.0.0.1"
    port: int = 8000


settings = Settings()
