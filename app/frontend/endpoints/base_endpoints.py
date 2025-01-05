from typing import Optional

from core.frontend import templates
from fastapi import APIRouter, Depends, Request
from fastapi.responses import FileResponse, HTMLResponse
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


@router.get(
    '/',
    response_class=HTMLResponse,
    summary='Загрузка главной страницы',
)
async def main_page(
    request: Request,
    user: User = Depends(get_user_on_jwt_from_cookies_or_redirect)
):
    context = {'request': request, 'user': user}
    return templates.TemplateResponse('index.html', context)
