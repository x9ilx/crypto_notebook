from typing import Optional

from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    app_title: str = 'Записная книжка для учёта криптовалюты'
    app_description: str = (
        'Позволяет вести учёт продажи/покупки криптовалюты и получить'
        'статистику: инвестиции, прибыль, активы и т. п.'
    )
    load_demo_data_fixtures: bool = False


class DBConfig(BaseModel):
    database_url: str = None
    echo: bool = False
    echo_pool: bool = False
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None


class SecurityConfig(BaseModel):
    secret: str = 'YOUR_SECRET_KEY'
    jwt_lifetime: int = 86400


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='APP_CONFIG__',
    )
    app: AppConfig = AppConfig()
    db: DBConfig = DBConfig()
    security: SecurityConfig = SecurityConfig()


settings = Settings()
