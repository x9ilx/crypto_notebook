from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routers import main_router
from core.config import settings

from frontend.exceptions import (
    FrontendUnauthorizedExeption,
    frontend_unauthorized_handler,
)
from frontend.routers import frontend_router
from services.users import create_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_user(
        email=settings.db.first_superuser_email,
        password=settings.db.first_superuser_password,
        is_superuser=True,
    )
    yield


app = FastAPI(
    title=settings.app.app_title,
    description=settings.app.app_description,
    lifespan=lifespan,
)
app.add_exception_handler(
    FrontendUnauthorizedExeption, frontend_unauthorized_handler
)
app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(main_router)
app.include_router(frontend_router)
