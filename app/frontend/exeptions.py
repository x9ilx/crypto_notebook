from fastapi import HTTPException
from fastapi.responses import RedirectResponse


class FrontendUnauthorizedExeption(HTTPException):
	pass


async def frontend_unauthorized_handler(*args):
	return RedirectResponse(url='/login')
