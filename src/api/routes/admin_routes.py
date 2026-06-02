from fastapi import APIRouter, HTTPException
from src.api.admin import AdminApi
from src.database.database import get_db
from src.repositories.purchase_repository import PurchaseRepository
from src.config.settings import DATABASE_NAME

router = APIRouter(prefix='/admin', tags=['admin'])

ADMIN_SESSIONS = {}

@router.post('/login')
def login(payload: dict):
    username = payload.get('username')
    password = payload.get('password')
    if not username or not password:
        raise HTTPException(status_code=400, detail='Missing credentials')
    return {'status': 'ok'}

@router.get('/api/purchases')
def purchases(wallet: str = None):
    conn = get_db(DATABASE_NAME)
    try:
        query = 'SELECT * FROM purchases WHERE 1=1'
        params = []
        if wallet:
            query += ' AND wallet LIKE ?'
            params.append(f'%{wallet}%')
        query += ' ORDER BY id DESC'
        rows = PurchaseRepository.search_purchases(conn, query, params)
        return AdminApi.purchases_logic(rows)
    finally:
        conn.close()

@router.put('/api/purchases/{pid}')
def update_purchase(pid: int, payload: dict):
    conn = get_db(DATABASE_NAME)
    try:
        fields = []
        values = []
        for key in ['wallet', 'amount', 'amount_eth', 'tokens_allocated', 'confirmed', 'tx_hash']:
            if key in payload:
                fields.append(f'{key}=?')
                values.append(payload[key])
        if not fields:
            raise HTTPException(status_code=400, detail='No fields provided')
        PurchaseRepository.update_purchase(conn, pid, fields, values)
        return {'status': 'updated'}
    finally:
        conn.close()

@router.delete('/api/purchases/{pid}')
def delete_purchase(pid: int):
    conn = get_db(DATABASE_NAME)
    try:
        PurchaseRepository.delete_purchase(conn, pid)
        return {'status': 'deleted'}
    finally:
        conn.close()

@router.get('/api/stats')
def stats():
    conn = get_db(DATABASE_NAME)
    try:
        return PurchaseRepository.get_stats(conn)
    finally:
        conn.close()