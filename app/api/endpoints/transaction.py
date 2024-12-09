from fastapi import APIRouter, Depends

router = APIRouter(
    prefix='/transaction', tags=['Транзакции и риск менеджмент']
)
