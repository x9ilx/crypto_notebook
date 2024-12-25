import pytest

from models.transaction import TransactionType


@pytest.fixture
def new_transaction_data():
    return {
        'amount': 10,
        'price': 0.1,
        'transaction_type': TransactionType.PURCHASE.name,
    }


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
