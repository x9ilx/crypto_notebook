import pytest

from models.transaction import TransactionType


TRANSACTION_URL = '/currency/' + '{currency_id}' + '/transaction'
TRANSACTION_DETAILS_URL = (
    '/currency/' + '{currency_id}' + '/transaction/' + '{transaction_id}'
)
TRANSACTION_PURCHASE_ENDPOINT = '/purchases'
TRANSACTION_SALE_ENDPOINT = '/sales'


CORRET_TRANSACTIONS_AND_ENPOINTS_LIST = [
    (
        {
            'amount': 10,
            'price': 0.1,
            'created_at': '2010-10-10',
            'transaction_type': TransactionType.PURCHASE.name,
        },
        TRANSACTION_PURCHASE_ENDPOINT,
    ),
    (
        {
            'amount': 10,
            'price': 0.1,
            'created_at': '2010-10-10',
            'transaction_type': TransactionType.SALE.name,
        },
        TRANSACTION_SALE_ENDPOINT,
    ),
]


@pytest.fixture
def transaction_expected_keys():
    return {
        'amount',
        'price',
        'id',
        'created_at',
        'risk_minimisation_point',
        'currency_id',
    }
