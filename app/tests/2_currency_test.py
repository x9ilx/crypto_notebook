from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

CURRENCY_URL = '/currency/'


class TestCreateCurrency:
    async def test_create_currency_no_authorized_user(
        self,
        new_currency_data,
        noauth_client: TestClient
    ):
        response = await noauth_client.post(
            url=CURRENCY_URL, json=new_currency_data
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Запрос должен вернуть ответ 401 - UNAUTHORIZED.'
        )


    async def test_create_currency_authorized_user(
        self,
        new_currency_data,
        currency_expected_keys,
        auth_client: TestClient
    ):
        response = await auth_client.post(
            url=CURRENCY_URL,
            json=new_currency_data
        )
        assert response.status_code == HTTPStatus.CREATED, (
            'Запрос должен вернуть ответ 201 - CREATED.'
        )
        result = response.json()
        missing_keys = currency_expected_keys - result.keys()
        assert not missing_keys, (
            f'В ответе не хватает следующих ключей: '
            f'`{"`, `".join(missing_keys)}`'
        )
        assert result['name'] == new_currency_data['name'].upper(), (
            'Название монеты не соответствует ожидаемому.'
        )
        assert result['description'] == new_currency_data['description'], (
            'Описание монеты не соответствует ожидаемому.'
        )
        assert result['quantity'] == new_currency_data['quantity'], (
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
        new_currency_data,
        invalid_name
    ):
        new_currency_data['name'] = invalid_name
        response = await auth_client.post(
            url=CURRENCY_URL,
            json=new_currency_data
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
            'Ответ на запрос должен быть 422 - UNPROCESSABLE ENTITY'
        )