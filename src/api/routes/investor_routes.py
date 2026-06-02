from fastapi import APIRouter

router = APIRouter(prefix='/api', tags=['investor'])

# Migration target:
# POST /buy
# POST /confirm
# GET /purchases
#
# Route handlers will be moved from main.py
# and wired to InvestorApi + PurchaseRepository.
