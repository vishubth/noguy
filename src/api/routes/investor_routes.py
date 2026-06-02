from fastapi import APIRouter, HTTPException

from src.api.investor import InvestorApi
from src.schemas.purchase import PurchaseRequest
from src.config.settings import TOKEN_RATE, ADMIN_WALLET

router = APIRouter(prefix='/api', tags=['investor'])


@router.post('/buy')
def buy(payload: PurchaseRequest):
    try:
        return InvestorApi.buy_logic(
            wallet=payload.wallet,
            amount_usd=payload.amount,
            token_rate=TOKEN_RATE,
            admin_wallet=ADMIN_WALLET,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# Remaining migration targets:
# POST /confirm
# GET /purchases
