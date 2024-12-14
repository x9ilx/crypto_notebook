import pytest
from conftest import override_db
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, select

from models.currency import Currency

from .user import user


@pytest.fixture
def new_currency_data():
    return {
        'name': 'NewCurrencyName',
        'description': 'New Currency Description',
        'quantity': 10.0,
    }


@pytest.fixture
def currency_expected_keys():
    return {
        'name',
        'description',
        'quantity',
        'id',
        'profit',
        'sales',
        'purchases',
        'risk_minimisation_points',
        'service_sales_points',
        'service_purchases_points',
    }


@pytest.fixture
async def generate_in_db_3_currencies():
    async for session in override_db():
        currencies = [
            Currency(
                id=i + 1,
                name=f'CURRENCY{i}',
                description=f'currency desc {i}',
                quantity=i,
                user_id=user.id,
            )
            for i in range(3)
        ]
        session.add_all(currencies)
        await session.commit()
        result = await session.execute(select(Currency))
        yield [
            jsonable_encoder(item) for item in result.scalars().unique().all()
        ]
        await session.execute(delete(Currency))
        await session.commit()


@pytest.fixture
async def generate_in_db_1_currencies():
    async for session in override_db():
        currency = Currency(
            name=f'CURRENCY',
            description=f'currency desc',
            quantity=500,
            user_id=user.id,
        )
        session.add(currency)
        await session.commit()
        result = await session.execute(select(Currency))
        yield jsonable_encoder(result.scalars().unique().first())
        await session.execute(delete(Currency))
        await session.commit()
