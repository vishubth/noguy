import os

DATABASE_NAME = os.getenv('DATABASE_NAME', 'presale.db')
TOKEN_RATE = int(os.getenv('TOKEN_RATE', '60000'))

# Add remaining environment variables here during final migration:
ADMIN_WALLET = "..."
ETHERSCAN_API_KEY = "..."
ADMIN_KEY = "..."
ADMIN_PASSWORD = "..."
