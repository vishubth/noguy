from src.services.purchase_service import PurchaseService
from src.services.blockchain_service import BlockchainService


class InvestorApi:

    @staticmethod
    def buy_logic(wallet, amount_usd, token_rate, admin_wallet):
        if not wallet or amount_usd <= 0:
            raise ValueError('Invalid wallet or amount')

        usd_to_eth = BlockchainService.get_live_usd_to_eth()
        amount_eth = round(amount_usd * usd_to_eth, 6)

        total_tokens = PurchaseService.calculate_tokens(
            amount_eth=amount_eth,
            token_rate=token_rate,
        )

        return PurchaseService.create_purchase_payload(
            wallet=wallet,
            eth_address=admin_wallet,
            amount_eth=amount_eth,
            total_tokens=total_tokens,
        )

    @staticmethod
    def confirm_logic(tx_hash, admin_wallet, expected_amount_eth, etherscan_api_key):
        return BlockchainService.verify_transaction(
            tx_hash=tx_hash,
            expected_wallet=admin_wallet,
            expected_amount_eth=expected_amount_eth,
            etherscan_api_key=etherscan_api_key,
        )

    @staticmethod
    def purchases_logic(rows):
        return [dict(row) for row in rows]
