from fastapi import APIRouter, HTTPException

from src.api.investor import InvestorApi
from src.schemas.purchase import PurchaseRequest, ConfirmRequest
from src.config.settings import TOKEN_RATE, ADMIN_WALLET, ETHERSCAN_API_KEY, DATABASE_NAME
from src.database.database import get_db
from src.repositories.purchase_repository import PurchaseRepository

router = APIRouter(prefix='/api', tags=['investor'])


@router.post('/buy')
def buy(payload: PurchaseRequest):
    conn = get_db(DATABASE_NAME)

    try:
        purchase = InvestorApi.buy_logic(
            wallet=payload.wallet,
            amount_usd=payload.amount,
            token_rate=TOKEN_RATE,
            admin_wallet=ADMIN_WALLET,
        )

        PurchaseRepository.create_purchase(
            conn,
            wallet=purchase['wallet'],
            amount=payload.amount,
            amount_eth=purchase['amount_eth'],
            tokens_allocated=purchase['tokens_allocated'],
        )

        return purchase

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        conn.close()


@router.post('/confirm')
def confirm(payload: ConfirmRequest):
    conn = get_db(DATABASE_NAME)

    try:
        purchase = PurchaseRepository.get_latest_purchase_by_wallet(
            conn,
            payload.wallet,
        )

        if not purchase:
            raise HTTPException(status_code=404, detail='No pending purchase found')

        verified = InvestorApi.confirm_logic(
            tx_hash=payload.tx_hash,
            admin_wallet=ADMIN_WALLET,
            expected_amount_eth=purchase['amount_eth'],
            etherscan_api_key=ETHERSCAN_API_KEY,
        )

        if verified:
            PurchaseRepository.confirm_purchase(
                conn,
                purchase['id'],
                payload.tx_hash,
            )

        return {'status': 'confirmed' if verified else 'unconfirmed'}

    finally:
        conn.close()


@router.get('/purchases')
def purchases(wallet: str, all: bool = False):
    if not wallet:
        raise HTTPException(status_code=400, detail='Wallet required')

    conn = get_db(DATABASE_NAME)

    try:
        rows = PurchaseRepository.get_purchases_by_wallet(
            conn,
            wallet,
            include_unconfirmed=all,
        )

        return InvestorApi.purchases_logic(rows)
    finally:
        conn.close()
