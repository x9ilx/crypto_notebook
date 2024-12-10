from http import HTTPStatus

import pytest

from models.currency import Currency

CURRENCY_URL = '/currency/'
CURRENCY_DETAILS_URL = CURRENCY_URL + '{currency_id}'


class TestCreateCurrency:
    async def test_get_all_currencies_noauth_user(
        self,
        noauth_client
    ):
        response = await noauth_client.get(
            url=CURRENCY_URL
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Ответ на запрос должен быть 401 - UNAUTHORIZED'
        )

    async def test_get_currency_details_auth_user(
        self,
        generate_in_db_1_currencies,
        currency_expected_keys,
        auth_client
    ):
        response = await auth_client.get(
            url=CURRENCY_DETAILS_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            )
        )
        result = response.json()
        assert response.status_code == HTTPStatus.OK, (
            'Ответ на запрос должен быть 200 - OK'
        )
        missing_keys = (
            currency_expected_keys - result.keys()
        )
        assert not missing_keys, (
            f'В ответе не хватает следующих ключей: '
            f'`{"`, `".join(missing_keys)}`.'
        )


    async def test_get_all_currencies_auth_user(
        self,
        generate_in_db_3_currencies,
        currency_expected_keys,
        auth_client
    ):
        response = await auth_client.get(
            url=CURRENCY_URL
        )
        result = response.json()
        assert response.status_code == HTTPStatus.OK, (
            'Ответ на запрос должен быть 200 - OK'
        )
        resut_len = len(result)
        currency_list_len = len(generate_in_db_3_currencies)
        assert resut_len == currency_list_len , (
            f'Было создано {currency_list_len} объектов, '
            f'было возвращено - {resut_len} объектов.'
        )
        for currency in result:
            missing_keys = currency_expected_keys - currency.keys()
            assert not missing_keys, (
                f'В ответе не хватает следующих ключей: '
                f'`{"`, `".join(missing_keys)}`.'
            )
        [item.pop('user_id') for item in generate_in_db_3_currencies]
        assert result == generate_in_db_3_currencies, (
            'Тело ответа отличается от ожидаемого.'
        )

    async def test_create_currency_no_authorized_user(
        self,
        new_currency_data,
        noauth_client
    ):
        response = await noauth_client.post(
            url=CURRENCY_URL, json=new_currency_data
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Ответ на запрос должен быть 401 - UNAUTHORIZED.'
        )


    async def test_create_currency_authorized_user(
        self,
        new_currency_data,
        currency_expected_keys,
        auth_client
    ):
        response = await auth_client.post(
            url=CURRENCY_URL,
            json=new_currency_data
        )
        assert response.status_code == HTTPStatus.CREATED, (
            'Ответ на запрос должен быть 201 - CREATED.'
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
            'Ответ на запрос должен быть 422 - UNPROCESSABLE ENTITY.'
        )


    @pytest.mark.parametrize(
        'invalid_quantity',
        [-1, 'str', None],
        ids=['negative', 'string', 'None']
    )
    async def test_create_currency_bad_quantity(
        self,
        auth_client,
        new_currency_data,
        invalid_quantity
    ):
        new_currency_data['quantity'] = invalid_quantity
        response = await auth_client.post(
            url=CURRENCY_URL,
            json=new_currency_data
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
            'Ответ на запрос должен быть 422 - UNPROCESSABLE ENTITY.'
        )


    async def test_create_currency_with_profit(
        self,
        auth_client,
        new_currency_data
    ):
        new_currency_data['profit'] = 100500
        response = await auth_client.post(
            url=CURRENCY_URL,
            json=new_currency_data
        )
        assert response.status_code == HTTPStatus.CREATED, (
            'Ответ на запрос должен быть 201 - CREATED.'
        )
        result = response.json()
        assert result['profit'] == 0, (
            'При попытке указать прибыль для новой монеты, '
            'прибыль должна остаться 0.'
        )