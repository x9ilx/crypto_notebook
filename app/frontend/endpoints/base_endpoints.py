from http import HTTPStatus
from typing import Optional

from core.frontend import templates
from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints.currency import currency_get_all
from core.db import get_async_session
from models.user import User
from services.frontend import get_user_on_jwt_from_cookies_or_redirect


router = APIRouter(tags=['frontend_base'])


@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('./static/images/favicon.ico')


@router.get(
    '/login',
    response_class=HTMLResponse,
    name='login_page',
    summary='Страница входа в админку'
)
async def login_page(request: Request, error: Optional[str] = None):
    context = {'request': request, 'error': error}
    return templates.TemplateResponse('login.html', context)


@router.post(
    '/logout_user',
    response_class=HTMLResponse,
    summary='Выход пользователя из системы'
)
async def logout_user(
    request: Request,
):
    response = RedirectResponse(
        request.url_for('login_page'),
        status_code=HTTPStatus.SEE_OTHER,
    )
    response.delete_cookie(key='jwt', httponly=True, secure=True)
    return response


@router.get(
    '/',
    response_class=HTMLResponse,
    summary='Загрузка главной страницы',
)
async def main_page(
    request: Request,
    name: str | None = None,
    user: User = Depends(get_user_on_jwt_from_cookies_or_redirect),
    session: AsyncSession = Depends(get_async_session)
):
    currencies = await currency_get_all(
        name=name,
        user=user,
        session=session
    )
    context = {'request': request, 'user': user, 'currencies': currencies}
    return templates.TemplateResponse('index.html', context)
