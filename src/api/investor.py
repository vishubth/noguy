from src.services.purchase_service import PurchaseService
from src.services.blockchain_service import BlockchainService

# Shadow migration module.
# Routes remain in main.py until final cutover.

class InvestorApi:

    @staticmethod
    def buy_logic():
        return 'Copied from main.py during migration phase'

    @staticmethod
    def confirm_logic():
        return 'Copied from main.py during migration phase'

    @staticmethod
    def purchases_logic():
        return 'Copied from main.py during migration phase'