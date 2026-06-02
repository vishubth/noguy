from fastapi import APIRouter, HTTPException

from src.api.investor import InvestorApi
from src.schemas.purchase import PurchaseRequest, ConfirmRequest
from src.config.settings import TOKEN_RATE, ADMIN_WALLET, ETHERSCAN_API_KEY

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


@router.post('/confirm')
def confirm(payload: ConfirmRequest):
    verified = InvestorApi.confirm_logic(
        tx_hash=payload.tx_hash,
        admin_wallet=ADMIN_WALLET,
        expected_amount_eth=0,
        etherscan_api_key=ETHERSCAN_API_KEY,
    )

    return {'status': 'confirmed' if verified else 'unconfirmed'}


# Remaining migration target:
# GET /purchases
