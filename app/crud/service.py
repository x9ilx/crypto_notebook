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


service_crud = CRUDRService()
