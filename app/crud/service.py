from crud.base import CRUDBase
from models.services import RiskMinimisation
from schemas.transaction import RiskMinimisationCreate, RiskMinimisationUpdate


class CRUDRiskMinimisation(
    CRUDBase[RiskMinimisation, RiskMinimisationCreate, RiskMinimisationUpdate]
):
    def __init__(self) -> None:
        super().__init__(RiskMinimisation)


risk_minimisation_crud = CRUDRiskMinimisation()
