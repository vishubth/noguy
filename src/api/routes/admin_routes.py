from fastapi import APIRouter

router = APIRouter(prefix='/admin', tags=['admin'])

# Migration target:
# POST /login
# GET /api/purchases
# POST /api/purchases
# PUT /api/purchases/{pid}
# DELETE /api/purchases/{pid}
# GET /api/stats
#
# Route handlers will be moved from main.py
# and wired to AdminApi + PurchaseRepository.
