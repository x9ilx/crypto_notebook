from http import HTTPStatus

import pytest

from tests.fixtures.currency import CURRENCY_URL, CURRENCY_DETAILS_URL


class TestCurrency:
    async def test_get_all_currencies_noauth_user(self, noauth_client):
        response = await noauth_client.get(url=CURRENCY_URL)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Ответ на запрос должен быть 401 - UNAUTHORIZED\n'
            f'content={response.content}'
        )

    async def test_get_currencies_noauth_user(
        self, generate_in_db_1_currencies, noauth_client
    ):
        response = await noauth_client.get(
            url=CURRENCY_DETAILS_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            )
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Ответ на запрос должен быть 401 - UNAUTHORIZED\n'
            f'content={response.content}'
        )

    async def test_get_currency_details_auth_user(
        self, generate_in_db_1_currencies, currency_expected_keys, auth_client
    ):
        response = await auth_client.get(
            url=CURRENCY_DETAILS_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            )
        )
        result = response.json()
        assert response.status_code == HTTPStatus.OK, (
            'Ответ на запрос должен быть 200 - OK\n'
            f'content={response.content}'
        )
        missing_keys = currency_expected_keys - result.keys()
        assert not missing_keys, (
            f'В ответе не хватает следующих ключей: '
            f'`{"`, `".join(missing_keys)}`.'
        )

    async def test_get_currency_details_another_user(
        self, generate_in_db_1_currencies_user2, auth_client
    ):
        response = await auth_client.get(
            url=CURRENCY_DETAILS_URL.format(
                currency_id=generate_in_db_1_currencies_user2['id']
            )
        )
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            'Ответ на запрос должен быть 404 - NOT FOUND\n'
            f'content={response.content}'
        )

    async def test_get_details_currency_wrong_id(self, auth_client):
        response = await auth_client.patch(
            url=CURRENCY_DETAILS_URL.format(currency_id='100500'), json={}
        )
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'Ответ на запрос должен быть 404 - NOT_FOUND.\n'
            f'content={response.content}'
        )

    async def test_get_all_currencies_auth_user(
        self, generate_in_db_3_currencies, currency_expected_keys, auth_client
    ):
        response = await auth_client.get(url=CURRENCY_URL)
        result = response.json()
        assert response.status_code == HTTPStatus.OK, (
            'Ответ на запрос должен быть 200 - OK\n'
            f'content={response.content}'
        )
        resut_len = len(result)
        currency_list_len = len(generate_in_db_3_currencies)
        assert resut_len == currency_list_len, (
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
        [item.pop('user') for item in generate_in_db_3_currencies]
        assert (
            result == generate_in_db_3_currencies
        ), 'Тело ответа отличается от ожидаемого.'

    async def test_create_currency_no_authorized_user(
        self, new_currency_data, noauth_client
    ):
        response = await noauth_client.post(
            url=CURRENCY_URL, json=new_currency_data
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Ответ на запрос должен быть 401 - UNAUTHORIZED.\n'
            f'content={response.content}'
        )

    async def test_create_currency_authorized_user(
        self, new_currency_data, currency_expected_keys, auth_client
    ):
        response = await auth_client.post(
            url=CURRENCY_URL, json=new_currency_data
        )
        assert response.status_code == HTTPStatus.CREATED, (
            'Ответ на запрос должен быть 201 - CREATED.\n'
            f'content={response.content}'
        )
        result = response.json()
        missing_keys = currency_expected_keys - result.keys()
        assert not missing_keys, (
            f'В ответе не хватает следующих ключей: '
            f'`{"`, `".join(missing_keys)}`'
        )
        assert (
            result['name'] == new_currency_data['name'].upper()
        ), 'Название монеты не соответствует ожидаемому.'
        assert (
            result['description'] == new_currency_data['description']
        ), 'Описание монеты не соответствует ожидаемому.'
        assert (
            result['quantity'] == new_currency_data['quantity']
        ), 'Количество монет не соответствует ожидаемому.'
        assert result['profit'] == 0.0, 'У новой монеты не может быть прибыли.'
        assert not result['sales'], 'У новой монеты не может быть продаж.'
        assert not result['purchases'], 'У новой монеты не может быть покупок.'
        assert not result[
            'risk_minimisation_points'
        ], 'У новой монеты не может быть точек минимизации рисков.'

    @pytest.mark.parametrize(
        'invalid_name',
        ['', '!@#%^&*()', '$', None],
        ids=['empty', 'bad symbols', '$ symbol', 'None'],
    )
    async def test_create_currency_bad_name(
        self, auth_client, new_currency_data, invalid_name
    ):
        new_currency_data['name'] = invalid_name
        response = await auth_client.post(
            url=CURRENCY_URL, json=new_currency_data
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
            'Ответ на запрос должен быть 422 - UNPROCESSABLE ENTITY.\n'
            f'content={response.content}'
        )

    @pytest.mark.parametrize(
        'invalid_quantity',
        [-1, 'str', None],
        ids=['negative', 'string', 'None'],
    )
    async def test_create_currency_bad_quantity(
        self, auth_client, new_currency_data, invalid_quantity
    ):
        new_currency_data['quantity'] = invalid_quantity
        response = await auth_client.post(
            url=CURRENCY_URL, json=new_currency_data
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
            'Ответ на запрос должен быть 422 - UNPROCESSABLE ENTITY.\n'
            f'content={response.content}'
        )

    async def test_create_currency_with_profit(
        self, auth_client, new_currency_data
    ):
        new_currency_data['profit'] = 100500
        response = await auth_client.post(
            url=CURRENCY_URL, json=new_currency_data
        )
        assert (
            response.status_code == HTTPStatus.CREATED
        ), 'Ответ на запрос должен быть 201 - CREATED.'
        result = response.json()
        assert result['profit'] == 0, (
            'При попытке указать прибыль для новой монеты, '
            'прибыль должна остаться 0.'
        )

    async def test_update_currency_noauth_user(
        self, generate_in_db_1_currencies, noauth_client
    ):
        response = await noauth_client.patch(
            url=CURRENCY_DETAILS_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            )
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Ответ на запрос должен быть 401 - UNAUTHORIZED\n'
            f'content={response.content}'
        )

    async def test_update_currency_wrong_id(self, auth_client):
        response = await auth_client.patch(
            url=CURRENCY_DETAILS_URL.format(currency_id='100500'), json={}
        )
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'Ответ на запрос должен быть 404 - NOT_FOUND.\n'
            f'content={response.content}'
        )

    @pytest.mark.parametrize(
        'update_data',
        [
            {'name': 'UPDATEDNAME', 'description': 'Updated Description'},
            {'name': 'UPDATEDNAME'},
            {'description': 'Updated Description'},
            {},
            {'name': 'UPDATEDNAME', 'description': 'null'},
        ],
        ids=[
            'full update',
            'name update',
            'description update',
            'empty',
            'description - null',
        ],
    )
    async def test_update_currency_authorized_user(
        self,
        generate_in_db_1_currencies,
        currency_expected_keys,
        update_data,
        auth_client,
    ):
        response = await auth_client.patch(
            url=CURRENCY_DETAILS_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            ),
            json=update_data,
        )
        assert response.status_code == HTTPStatus.OK, (
            'Ответ на запрос должен быть 200 - OK.\n'
            f'content={response.content}'
        )
        result = response.json()
        missing_keys = currency_expected_keys - result.keys()
        assert not missing_keys, (
            f'В ответе не хватает следующих ключей: '
            f'`{"`, `".join(missing_keys)}`'
        )
        if 'name' in update_data:
            assert (
                result['name'] == update_data['name'].upper()
            ), 'Название монеты не соответствует ожидаемому.'
        if 'description' in update_data:
            if update_data['description'] == 'null':
                update_data['description'] = None
            assert (
                result['description'] == update_data['description']
            ), 'Описание монеты не соответствует ожидаемому.'
        assert (
            result['quantity'] == generate_in_db_1_currencies['quantity']
        ), 'Количество монет не соответствует ожидаемому.'
        assert (
            result['profit'] == generate_in_db_1_currencies['profit']
        ), 'Значение прибыли не соответствует ожидаемому.'
        assert not result[
            'sales'
        ], 'Список продаж монеты не соответствует ожидаемому'
        assert not result[
            'purchases'
        ], 'Список покупок монеты не соответствует ожидаемому'
        assert not result[
            'risk_minimisation_points'
        ], 'Список минимизации рисков монеты не соответствует ожидаемому'

    async def test_get_all_currencies_noauth_user(
        self, generate_in_db_1_currencies, noauth_client
    ):
        response = await noauth_client.delete(
            url=CURRENCY_DETAILS_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            )
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Ответ на запрос должен быть 401 - UNAUTHORIZED\n'
            f'content={response.content}'
        )

    async def test_delete_currency_wrong_id(self, auth_client):
        response = await auth_client.delete(
            url=CURRENCY_DETAILS_URL.format(currency_id='100500')
        )
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            f'Ответ на запрос должен быть 404 - NOT_FOUND.\n'
            f'content={response.content}'
        )

    async def test_delete_currency_auth_user(
        self, generate_in_db_1_currencies, currency_expected_keys, auth_client
    ):
        response = await auth_client.delete(
            url=CURRENCY_DETAILS_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            )
        )
        assert response.status_code == HTTPStatus.OK, (
            f'Ответ на запрос должен быть 200 - OK.\n'
            f'content={response.content}'
        )
        delete_result = response.json()
        generate_in_db_1_currencies.pop('user')
        generate_in_db_1_currencies.pop('user_id')
        missing_keys = currency_expected_keys - delete_result.keys()
        assert not missing_keys, (
            f'В ответе не хватает следующих ключей: '
            f'`{"`, `".join(missing_keys)}`'
        )
        assert generate_in_db_1_currencies == delete_result, (
            'При удалении вернулись неверные данные. '
            'Возможно удалён не тот объект'
        )
