from typing import Optional

from core.frontend import templates
from core.users import current_user
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from models.user import User


router = APIRouter(tags=['frontend_base'])


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
    # user: User = Depends(current_user)
):
    context = {'request': request}
    return templates.TemplateResponse('index.html', context)
