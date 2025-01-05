from fastapi import HTTPException, Request
from fastapi.responses import RedirectResponse


class FrontendUnauthorizedExeption(HTTPException):
    pass


async def frontend_unauthorized_handler(*args):
    return RedirectResponse(url='/login')