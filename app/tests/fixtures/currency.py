import pytest
from conftest import override_db
from fastapi.encoders import jsonable_encoder
from sqlalchemy import delete, select

from models.currency import Currency
from models.user import User

from .user import user, user2


CURRENCY_URL = '/currency/'
CURRENCY_DETAILS_URL = CURRENCY_URL + '{currency_id}'


def generate_currency(name: str, current_user: User):
	return Currency(
		name=name,
		description='currency desc',
		quantity=500,
		user_id=current_user.id,
	)


async def delete_all_currencies():
	async for session in override_db():
		await session.execute(delete(Currency))
		await session.commit()


async def create_currency_in_db(currency: Currency):
	async for session in override_db():
		session.add(currency)
		await session.commit()
		result = await session.execute(select(Currency))
		yield jsonable_encoder(result.scalars().unique().first())
		await delete_all_currencies()


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
	async for currency in create_currency_in_db(
		generate_currency(name='CURRENCYUSER1', current_user=user)
	):
		yield currency


@pytest.fixture
async def generate_in_db_1_currencies_user2():
	async for currency in create_currency_in_db(
		generate_currency(name='CURRENCYUSER2', current_user=user2)
	):
		yield currency


@pytest.fixture
async def get_currency_from_db():
	async def make_get_currency_from_db(currency_id: int = 1):
		async for session in override_db():
			result = await session.execute(
				select(Currency).where(Currency.id == currency_id)
			)
			return result.scalars().first()

	return make_get_currency_from_db
