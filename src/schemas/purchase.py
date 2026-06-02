from pydantic import BaseModel

class PurchaseRequest(BaseModel):
    wallet: str
    amount: float

class ConfirmRequest(BaseModel):
    wallet: str
    tx_hash: str