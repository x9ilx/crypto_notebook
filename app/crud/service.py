import operator

from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.currency import Currency
from models.services import RiskMinimisation, Service
from models.transaction import TransactionType
from models.user import User
from schemas.service import (
    RiskMinimisationCreate,
    RiskMinimisationUpdate,
    ServiceCreate,
    ServiceUpdate,
)


class CRUDRiskMinimisation(
        CRUDBase[RiskMinimisation, RiskMinimisationCreate,
                 RiskMinimisationUpdate]
):
    def __init__(self) -> None:
        super().__init__(RiskMinimisation)


risk_minimisation_crud = CRUDRiskMinimisation()


class CRUDRService(CRUDBase[Service, ServiceCreate, ServiceUpdate]):
    def __init__(self) -> None:
        super().__init__(Service)

    async def create_service(
            self,
            currency: Currency,
            new_service: ServiceCreate,
            transaction_type: TransactionType,
            user: User,
            session: AsyncSession,
    ) -> Service:
        service_list = (
            currency.service_purchases_points
            if transaction_type == TransactionType.PURCHASE
            else currency.service_sales_points
        )
        service = Service(
            service_type=transaction_type,
            user_id=user.id,
            currency_id=currency.id,
            investments=new_service.investments,
            price=new_service.price,
        )
        service_list.append(service)
        return await self._commit_and_refresh(obj=service, session=session)

    async def get_amount_investment_and_expected_currency(
            self,
            currency: Currency,
            service_type: TransactionType,
    ) -> dict[str, float]:
        if service_type == TransactionType.PURCHASE:
            operation = operator.truediv
            service_list = currency.service_purchases_points
        else:
            operation = operator.mul
            service_list = currency.service_sales_points

        result = {
			'total_investments': 0,
			'total_profit': 0,
		}
        for service in service_list:
            result['total_investments'] += service.investments
            result['total_profit'] += operation(
                service.investments,
                service.price
            )
        return result


service_crud = CRUDRService()
