from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

CURRENCY_URL = '/currency/'


class TestCreateCurrency:
    async def test_create_currency_no_authorized_user(
        self,
        noauth_client: TestClient
    ):
        currency_data = {
            'name': 'New Currency Name',
            'description': 'New Currency Description',
            'quantity': 10.0
        }
        response = await noauth_client.post(
            url=CURRENCY_URL, json=currency_data
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Запрос должен вернуть ответ 401 - UNAUTHORIZED.'
        )


    async def test_create_currency_authorized_user(
        self,
        auth_client: TestClient
    ):
        currency_data = {
            'name': 'New Currency Name',
            'description': 'New Currency Description',
            'quantity': 10.0
        }
        expected_keys = {
            'name',
            'description',
            'quantity',
            'id',
            'profit',
            'sales',
            'purchases',
            'risk_points',
        }
        response = await auth_client.post(
            url=CURRENCY_URL,
            json=currency_data
        )
        print(response.content)
        assert response.status_code == HTTPStatus.CREATED, (
            'Запрос должен вернуть ответ 201 - CREATED.'
        )
        result = response.json()
        missing_keys = expected_keys - result.keys()
        assert not missing_keys, (
            f'В ответе не хватает следующих ключей: '
            f'`{"`, `".join(missing_keys)}`'
        )
        assert result['name'] == currency_data['name'].upper(), (
            'Название монеты не соответствует ожидаемому.'
        )
        assert result['description'] == currency_data['description'], (
            'Описание монеты не соответствует ожидаемому.'
        )
        assert result['quantity'] == currency_data['quantity'], (
            'Количество монет не соответствует ожидаемому.'
        )
        assert result['profit'] == 0.0, 'У новой монеты не может быть прибыли.'
        assert not result['sales'], 'У новой монеты не может быть продаж.'
        assert not result['purchases'], 'У новой монеты не может быть покупок.'
        assert not result['risk_points'], (
            'У новой монеты не может быть точек минимизации рисков.'
        )


    @pytest.mark.parametrize(
        'invalid_name',
        ['', '!@#%^&*()', '$', None],
        ids=['empty', 'bad symbols', '$ symbol', 'None']
    )
    async def test_create_currency_bad_name(
        self,
        auth_client,
        invalid_name
    ):
        currency_data = {
            'name': invalid_name,
            'description': 'New Currency Description',
            'quantity': 10.0
        }
        currency_data['name'] = invalid_name
        response = await auth_client.post(
            url=CURRENCY_URL,
            json=currency_data
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
            'Ответ на запрос должен быть 422 - UNPROCESSABLE ENTITY'
        )