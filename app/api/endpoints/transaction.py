from fastapi import APIRouter, Depends

from schemas.transaction import TransactionResponse

router = APIRouter(
    prefix='/transaction', tags=['Транзакции']
)


@router.get(
    '/',
    response_model=list[TransactionResponse],
    summary='Позволяет получить все монеты пользователя.',
)
async def currency_get(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[TransactionResponse]:
    return await currency_crud.get_all(user=user, session=session)


@router.get(
    '/{currency_id}',
    response_model=CurrencyResponse,
    summary='Позволяет получить информацию о монете.',
)
async def currency_get(
    currency_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> CurrencyResponse:
    return await check_currency_exist(
        currency_id=currency_id, user=user, session=session
    )


@router.post(
    '/',
    response_model=CurrencyResponse,
    summary='Позволяет добавить новую монету в базу.',
    status_code=HTTPStatus.CREATED
)
async def currency_create(
    currency: CurrencyCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> CurrencyResponse:
    return await currency_crud.create(currency, user, session)


@router.patch(
    '/{currency_id}',
    response_model=CurrencyResponse,
    summary='Позволяет обновить информацию о монете.',
    description='Для установки пустого значения необходимо отправить null'
)
async def currency_update(
    currency_id: int,
    currency: CurrencyUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await currency_crud.update(
        db_obj=await check_currency_exist(
            currency_id=currency_id,
            user=user,
            session=session
        ),
        obj_in=currency,
        session=session
    )


@router.delete(
    '/{currency_id}',
    response_model=CurrencyResponse,
    summary='Позволяет удалить монету из базы.'
)
async def currency_delete(
    currency_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> CurrencyResponse:
    return await currency_crud.delete(
        await check_user_is_owner(
            currency_id=currency_id, user=user, session=session
        ),
        session,
    )
