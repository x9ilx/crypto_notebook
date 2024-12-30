from http import HTTPStatus

import pytest

from crud.transaction import RISK_MINIMAISATION_MULTIPLER
from models.transaction import TransactionType

TRANSACTION_URL = '/currency/' + '{currency_id}' + '/transaction'
TRANSACTION_DETAILS_URL = (
    '/currency/' + '{currency_id}' + '/transaction/' + '{transaction_id}'
)
TRANSACTION_PURCHASE_ENDPOINT = '/purchases'
TRANSACTION_SALE_ENDPOINT = '/sales'


class TestTransaction:
    async def test_create_currency_no_authorized_user(
        self,
        generate_in_db_1_currencies,
        new_purchase_transaction_data,
        noauth_client
    ):
        response = await noauth_client.post(
            url=TRANSACTION_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            ),
            json=new_purchase_transaction_data,
        )
        assert response.status_code == HTTPStatus.NOT_FOUND, (
            'Ответ на запрос должен быть 404 - NOT FOUND.\n'
            f'content={response.content}'
        )

    @pytest.mark.parametrize(
        'transaction_data, endpoint',
        [
            (
                {
                    'amount': 10,
                    'price': 0.1,
                    'transaction_type': TransactionType.PURCHASE.name,
                },
                TRANSACTION_PURCHASE_ENDPOINT,
            ),
            (
                {
                    'amount': 10,
                    'price': 0.1,
                    'transaction_type': TransactionType.SALE.name,
                },
                TRANSACTION_SALE_ENDPOINT,
            ),
        ],
        ids=['purchase', 'sale'],
    )
    async def test_create_transaction_authorized_user(
        self,
        freeze_data,
        generate_in_db_1_currencies,
        transaction_expected_keys,
        risk_minimisation_expected_keys,
        transaction_data,
        endpoint,
        auth_client,
    ):
        response = await auth_client.post(
            url=TRANSACTION_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            )
            + endpoint,
            json=transaction_data,
        )
        assert response.status_code == HTTPStatus.OK, (
            'Ответ на запрос должен быть 200 - OK.\n'
            f'content={response.content}'
        )
        result = response.json()
        missing_keys = transaction_expected_keys - result.keys()
        assert not missing_keys, (
            f'В ответе не хватает следующих ключей: '
            f'`{"`, `".join(missing_keys)}`'
        )
        assert (
            result['currency_id'] == generate_in_db_1_currencies['id']
        ), 'Транзакция привязана не к той монете.'
        assert (
            result['amount'] == transaction_data['amount']
        ), 'Количество монет не соответствует ожидаемому.'
        assert (
            result['price'] == transaction_data['price']
        ), 'Стоимость монет не соответствует ожидаемому.'
        assert result['created_at'] == str(freeze_data).replace(
            ' ', 'T'
        ), 'Дата создания транзакции не соответствует ожидаемой.'
        if endpoint == TRANSACTION_PURCHASE_ENDPOINT:
            assert result['risk_minimisation_point'], (
                f'При создании транзакции типа "покупка '
                f'({TransactionType.PURCHASE})" '
                f'должна формироваться точка минимизации рисков'
            )
        if result['risk_minimisation_point'] and len(
            result['risk_minimisation_point']
        ):
            risk_minimisation_missing_keys = (
                risk_minimisation_expected_keys
                - set(result['risk_minimisation_point'])
            )
            assert not risk_minimisation_missing_keys, (
                f'В минимизации рисков не хватает следующих ключей: '
                f'`{"`, `".join(risk_minimisation_missing_keys)}`'
            )
            assert result['risk_minimisation_point']['price'] == (
                transaction_data['price'] * RISK_MINIMAISATION_MULTIPLER
            ), 'Цена точки минимизации рисков рассчитывается неверно.'
            assert result['risk_minimisation_point']['transaction_id'] == (
                result['id']
            ), 'Точки минимизации рисков привязана не к той транзакции.'
            assert result['risk_minimisation_point']['transaction_id'] == (
                result['id']
            ), 'Точки минимизации рисков привязана не к той транзакции.'
            assert result['risk_minimisation_point']['currency_id'] == (
                generate_in_db_1_currencies['id']
            ), 'Точки минимизации рисков привязана не к той монете.'


    async def test_change_currency_quantity_on_purchase_transaction(
        self,
        generate_in_db_1_currencies,
        get_currency_from_db,
        new_purchase_transaction_data,
        auth_client,
    ):
        old_currency_quantitty = generate_in_db_1_currencies['quantity']
        response = await auth_client.post(
            url=TRANSACTION_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            )
            + TRANSACTION_PURCHASE_ENDPOINT,
            json=new_purchase_transaction_data,
        )
        assert response.status_code == HTTPStatus.OK, (
            'Ответ на запрос должен быть 200 - OK.\n'
            f'content={response.content}'
        )
        currency = await get_currency_from_db(
            currency_id=generate_in_db_1_currencies['id']
        )
        assert currency.quantity == (
            old_currency_quantitty + new_purchase_transaction_data['amount']
        ), (
            'При покупке монеты количество должно '
            'увеличить на на количество при покупке.'
        )

    async def test_change_currency_quantity_on_sale_transaction(
        self,
        generate_in_db_1_currencies,
        get_currency_from_db,
        new_sale_transaction_data,
        auth_client,
    ):
        old_currency_quantitty = generate_in_db_1_currencies['quantity']
        response = await auth_client.post(
            url=TRANSACTION_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            )
            + TRANSACTION_SALE_ENDPOINT,
            json=new_sale_transaction_data,
        )
        assert response.status_code == HTTPStatus.OK, (
            'Ответ на запрос должен быть 200 - OK.\n'
            f'content={response.content}'
        )
        currency = await get_currency_from_db(
            currency_id=generate_in_db_1_currencies['id']
        )
        assert currency.quantity == (
            old_currency_quantitty - new_sale_transaction_data['amount']
        ), (
            'При продаже монеты количество должно '
            'уменьшиться на количество при покупке.'
        )

    async def test_sell_more_than_have(
        self,
        generate_in_db_1_currencies,
        new_sale_transaction_data,
        auth_client,
    ):
        new_sale_transaction_data['amount'] = (
            generate_in_db_1_currencies['quantity'] * 2
        )
        response = await auth_client.post(
            url=TRANSACTION_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            )
            + TRANSACTION_SALE_ENDPOINT,
            json=new_sale_transaction_data,
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Ответ на запрос должен быть 400 - BAD REQUEST.\n'
            f'content={response.content}'
        )

    @pytest.mark.parametrize(
        'transaction_data',
        [
            {
                'amount': -1,
                'price': 0.1,
                'transaction_type': TransactionType.PURCHASE.name,
            },
            {
                'amount': 0,
                'price': 0.1,
                'transaction_type': TransactionType.PURCHASE.name,
            },
            {
                'price': 0.1,
                'transaction_type': TransactionType.PURCHASE.name,
            },
                        {
                'amount': 1,
                'price': -1,
                'transaction_type': TransactionType.PURCHASE.name,
            },
            {
                'amount': 1,
                'price': 0,
                'transaction_type': TransactionType.PURCHASE.name,
            },
            {
                'amount': 1,
                'transaction_type': TransactionType.PURCHASE.name,
            },
            {
                'transaction_type': TransactionType.PURCHASE.name,
            }
        ],
        ids=[
            'negative amount',
            'zero amount',
            'no amount',
            'negative price',
            'zero price',
            'no price',
            'no amount, no price'
        ],
    )
    async def test_create_transaction_bad_params(
        self,
        generate_in_db_1_currencies,
        transaction_data,
        auth_client,
    ):
        response = await auth_client.post(
            url=TRANSACTION_URL.format(
                currency_id=generate_in_db_1_currencies['id']
            )
            + TRANSACTION_PURCHASE_ENDPOINT,
            json=transaction_data,
        )
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, (
            'Ответ на запрос должен быть 422 - UNPROCESSABLE ENTITY.\n'
            f'content={response.content}'
        )