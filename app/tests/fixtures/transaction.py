import pytest

from models.transaction import TransactionType


@pytest.fixture
def new_purchase_transaction_data(freezer):
    return {
        'amount': 10,
        'price': 0.1,
        'create_at': freezer,
        'transaction_type': TransactionType.PURCHASE.name,
    }


@pytest.fixture
def new_sale_transaction_data(freezer):
    return {
        'amount': 10,
        'price': 0.1,
        'create_at': freezer,
        'transaction_type': TransactionType.SALE.name,
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
