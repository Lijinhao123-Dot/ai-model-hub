"""应用配置"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用设置"""
    # 数据库
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/ai_model_hub"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # 文件存储
    MAX_FILE_SIZE: int = 5368709120  # 5GB
    UPLOAD_DIR: str = "./uploads"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
