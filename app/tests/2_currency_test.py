from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response
from schemas.currency import CurrencyCreate, CurrencyResponse

CURRENCY_URL = '/currency/'


class TestCreateCurrency:
    async def test_create_currency_no_authorized_user_unauthorized(
        self,
        noauth_client: TestClient,
        new_currency_schema: CurrencyCreate
    ) -> None:
        response: Response = await noauth_client.post(
            url=CURRENCY_URL, json=new_currency_schema.model_dump()
        )
        assert (
            response.status_code == HTTPStatus.UNAUTHORIZED,
            
        )


    async def test_create_currency_authorized_user_ok(
        self,
        auth_client: TestClient,
        new_currency_schema: CurrencyCreate
    ) -> None:
        response: Response = await auth_client.post(
            url=CURRENCY_URL,
            json=new_currency_schema.model_dump()
        )
        assert (
            response.status_code == HTTPStatus.CREATED,
            'Запрос должен вернуть ответ 201 - CREATED.'
        )
        result: CurrencyResponse = CurrencyResponse(**response.json())
        assert (result.name == new_currency_schema.name,
            'Название монеты не соответствует ожидаемому.'
        )
        assert (result.description == new_currency_schema.description,
            'Описание монеты не соответствует ожидаемому.'
        )
        assert (result.quantity == new_currency_schema.quantity,
            'Количество монет не соответствует ожидаемому.'
        )
        assert (result.profit == 0.0,
            'У новой монеты не может быть прибыли.'
        )
        assert (result.sales == [],
            'У новой монеты не может быть продаж.'
        )
        assert (result.purchases == [],
            'У новой монеты не может быть покупок.'
        )
        assert (result.risk_points == [],
            'У новой монеты не может быть точек минимизации рисков.'
        )
