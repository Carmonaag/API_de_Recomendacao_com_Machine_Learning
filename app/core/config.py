from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/recommendations"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600  # 1 hora

    # ML
    CF_MODEL_PATH: str = str(BASE_DIR / "models/cf_model.joblib")
    CB_MODEL_PATH: str = str(BASE_DIR / "models/cb_model.joblib")
    MODEL_VERSION: str = "v1"
    MIN_INTERACTIONS: int = 5

    # Monitoring
    ENABLE_MONITORING: bool = True
    METRICS_PORT: int = 9090

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

settings = Settings()