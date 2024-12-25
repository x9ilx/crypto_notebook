import pytest


@pytest.fixture
def risk_minimisation_expected_keys():
    return {'id', 'price', 'transaction_id', 'currency_id'}
