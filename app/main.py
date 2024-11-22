from contextlib import asynccontextmanager

from api.routers import main_router
from core.config import settings
from core.db import async_session_maker
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# from frontend.routers import frontend_router
from services.users import create_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_user(
        email=settings.db.first_superuser_email,
        name='Администратор',
        telegram_user_id=settings.db.first_superuser_tg_id,
        password=settings.db.first_superuser_password,
        is_superuser=True,
        is_manager=True,
    )
    yield


app = FastAPI(
    title=settings.app.app_title,
    description=settings.app.app_description,
    lifespan=lifespan,
)
app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(main_router)
# app.include_router(frontend_router)
