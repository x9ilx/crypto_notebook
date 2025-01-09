from http import HTTPStatus

from fastapi import Depends, Request

from core.users import get_jwt_strategy, get_user_manager
from frontend.exeptions import FrontendUnauthorizedExeption
from models.user import User


async def get_user_on_jwt_from_cookies_or_redirect(
	request: Request, user_manager=Depends(get_user_manager)
) -> User:
	jwt_strategy = get_jwt_strategy()
	user = await jwt_strategy.read_token(
		token=request.cookies.get('jwt'), user_manager=user_manager
	)
	if user:
		return user
	raise FrontendUnauthorizedExeption(status_code=HTTPStatus.UNAUTHORIZED)
