from http import HTTPStatus

from core.frontend import templates
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.currency_validators import check_currency_exist
from core.db import get_async_session
from models.currency import Currency
from models.user import User
from services.frontend import get_user_on_jwt_from_cookies_or_redirect

router = APIRouter(prefix='/currency', tags=['frontend_currency'])


@router.get(
        '/{currency_id}',
        response_class=HTMLResponse,
        summary='Загрузста страницы с информацией о монете.',

)
async def main_page(
        request: Request,
        currency_id: int,
        user: User = Depends(get_user_on_jwt_from_cookies_or_redirect),
        session: AsyncSession = Depends(get_async_session)
):
    error = ''
    currency = None
    try:
        currency = await check_currency_exist(
                currency_id=currency_id,
                user=user,
                session=session
        )
    except HTTPException as e:
        if e.status_code == HTTPStatus.NOT_FOUND:
            error = e.detail
    print(error)
    context = {
        'request': request,
        'user': user,
        'currency': currency,
        'error': error,
    }
    return templates.TemplateResponse('currency_page.html', context)
