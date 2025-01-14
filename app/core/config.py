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
	images_save_base_path: str = 'static/images/'
	allowed_mime_type_for_currency_image: str = ['image/jpeg', 'image/png']

class DBConfig(BaseModel):
	database_url: str = None
	echo: bool = False
	echo_pool: bool = False
	first_superuser_email: Optional[EmailStr] = None
	first_superuser_password: Optional[str] = None


class SecurityConfig(BaseModel):
	secret: str = 'YOUR_SECRET_KEY'
	jwt_lifetime: int = 86400


class EmailConfig(BaseModel):
	mail_username: str = (None,)
	mail_password: str = (None,)
	mail_from: str = ('scid_bot_1@admin.com',)
	mail_port: int = (587,)
	mail_server: str = (None,)
	mail_from_name: str = ('scid_bot_1',)
	mail_starttls: bool = (True,)
	mail_ssl_tls: bool = (False,)
	use_credentials: bool = (True,)
	validate_certs: bool = True


class Settings(BaseSettings):
	model_config = SettingsConfigDict(
		env_ignore_empty=True,
		env_file='.env',
		env_file_encoding='utf-8',
		case_sensitive=False,
		env_nested_delimiter='__',
		env_prefix='APP_CONFIG__',
	)
	app: AppConfig = AppConfig()
	db: DBConfig = DBConfig()
	security: SecurityConfig = SecurityConfig()
	email: EmailConfig = EmailConfig()


settings = Settings()
