from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import requests
import json
import os


# -------------------------------
# GET ETH PRICE (Coingecko)
# -------------------------------
def get_live_usd_to_eth():
    """Try Binance first, fallback to Coinbase"""
    try:
        res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT", timeout=10)
        res.raise_for_status()
        eth_usd = float(res.json()["price"])
    except Exception:
        try:
            res = requests.get("https://api.coinbase.com/v2/prices/ETH-USD/spot", timeout=10)
            res.raise_for_status()
            eth_usd = float(res.json()["data"]["amount"])
        except Exception as e:
            print("⚠️ Both Binance & Coinbase failed:", e)
            return 0.00052
    return round(1 / eth_usd, 8)



# -------------------------------
# CONFIG
# -------------------------------
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

DB = "presale.db"
ADMIN_WALLET = "0xE562539aC11a45aC9D37C779A33D1b571e49f272"  # Your ETH wallet
ETHERSCAN_API_KEY = "PUA9B1D9WGH3PCMPD94NKHT1VQUJ8YWEFM"
TOKEN_RATE = 60000  # 1 ETH = 60,000 tokens

# -------------------------------
# DATABASE SETUP
# -------------------------------
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def startup():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wallet TEXT,
            amount REAL,
            amount_eth REAL,
            tokens_allocated REAL,
            tx_hash TEXT,
            confirmed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# -------------------------------
# ROUTES - PAGES
# -------------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Landing page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/user-panel", response_class=HTMLResponse)
def user_panel(request: Request):
    """Buy Coin page"""
    return templates.TemplateResponse("user-panel.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    """User-specific dashboard page"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

# -------------------------------
# ROUTES - API
# -------------------------------
@app.post("/api/buy")
async def buy(request: Request):
    """Create pending purchase"""
    data = await request.json()
    wallet = data.get("wallet")
    amount = float(data.get("amount", 0))
    if not wallet or amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid wallet or amount")

    USD_TO_ETH = get_live_usd_to_eth()  # conversion rate (USD → ETH)
    amount_eth = round(amount * USD_TO_ETH, 6)
    tokens_allocated = round(amount_eth * TOKEN_RATE, 2)
    bonus = 1.2
    total_tokens = round(tokens_allocated * bonus, 2)

    conn = get_db()
    conn.execute("""
        INSERT INTO purchases (wallet, amount, amount_eth, tokens_allocated)
        VALUES (?, ?, ?, ?)
    """, (wallet, amount, amount_eth, total_tokens))
    conn.commit()
    conn.close()

    return JSONResponse({
        "wallet": wallet,
        "eth_address": ADMIN_WALLET,
        "amount_eth": amount_eth,
        "tokens_allocated": total_tokens
    })

# -------------------------------
# VERIFY TX HASH (Etherscan)
# -------------------------------
def verify_transaction(tx_hash: str, expected_wallet: str, expected_amount_eth: float) -> bool:
    """Check if tx is confirmed and sent to admin wallet"""
    try:
        url = f"https://api.etherscan.io/api"
        params = {
            "module": "transaction",
            "action": "gettxreceiptstatus",
            "txhash": tx_hash,
            "apikey": ETHERSCAN_API_KEY
        }
        res = requests.get(url, params=params, timeout=10).json()
        if res.get("status") != "1":
            return False

        # Optional deeper check: get transaction details
        tx_url = f"https://api.etherscan.io/api"
        tx_params = {
            "module": "proxy",
            "action": "eth_getTransactionByHash",
            "txhash": tx_hash,
            "apikey": ETHERSCAN_API_KEY
        }
        tx_data = requests.get(tx_url, params=tx_params, timeout=10).json()
        tx = tx_data.get("result")
        if not tx:
            return False

        to_address = tx.get("to", "").lower()
        if to_address != expected_wallet.lower():
            return False

        # Convert from hex to ETH value
        value_wei = int(tx.get("value", "0x0"), 16)
        value_eth = value_wei / 1e18
        return value_eth >= expected_amount_eth * 0.95  # allow ~5% margin
    except Exception as e:
        print("Verify error:", e)
        return False

# -------------------------------
# API: Confirm Payment
# -------------------------------
@app.post("/api/confirm")
async def confirm_payment(request: Request):
    """User submits TX hash for verification"""
    data = await request.json()
    wallet = data.get("wallet")
    tx_hash = data.get("tx_hash")

    if not wallet or not tx_hash:
        raise HTTPException(status_code=400, detail="Wallet and tx hash required")

    conn = get_db()
    # Get the last pending purchase for this wallet
    row = conn.execute(
        "SELECT * FROM purchases WHERE wallet=? ORDER BY id DESC LIMIT 1", (wallet,)
    ).fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="No pending purchase found")

    ok = verify_transaction(tx_hash, ADMIN_WALLET, row["amount_eth"])
    if ok:
        conn.execute(
            "UPDATE purchases SET confirmed=1, tx_hash=? WHERE id=?",
            (tx_hash, row["id"])
        )
        conn.commit()
        conn.close()
        return JSONResponse({"status": "confirmed"})
    else:
        conn.close()
        return JSONResponse({"status": "unconfirmed"})

# -------------------------------
# API: Fetch purchases for a wallet
# -------------------------------
@app.get("/api/purchases")
def get_purchases(wallet: str, all: bool = False):
    """Return purchases for a wallet (confirmed only by default)"""
    if not wallet:
        raise HTTPException(status_code=400, detail="Wallet required")

    conn = get_db()
    if all:
        data = conn.execute("""
            SELECT id, wallet, amount, amount_eth, tokens_allocated, tx_hash, confirmed, created_at
            FROM purchases WHERE wallet=? ORDER BY created_at DESC
        """, (wallet,)).fetchall()
    else:
        data = conn.execute("""
            SELECT id, wallet, amount, amount_eth, tokens_allocated, tx_hash, confirmed, created_at
            FROM purchases WHERE wallet=? AND confirmed=1 ORDER BY created_at DESC
        """, (wallet,)).fetchall()
    conn.close()

    return JSONResponse([dict(row) for row in data])





