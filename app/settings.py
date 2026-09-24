from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/marketmind.db"
    market_config_path: str = "configs/markets.yaml"
    data_stale_after_hours: int = 48
    minimum_rows_for_report: int = 30
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def ensure_data_directory(self) -> None:
        if self.database_url.startswith("sqlite:///"):
            Path(self.database_url.removeprefix("sqlite:///")).parent.mkdir(parents=True, exist_ok=True)

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_data_directory()
    return settings
