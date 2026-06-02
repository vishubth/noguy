import os

DB = os.getenv('DB_PATH', 'presale.db')

ADMIN_WALLET = os.getenv('ADMIN_WALLET', '')
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY', '')
TOKEN_RATE = int(os.getenv('TOKEN_RATE', '60000'))

ADMIN_KEY = os.getenv('ADMIN_KEY', '')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '')
