class PurchaseService:

    @staticmethod
    def calculate_tokens(amount_eth, token_rate, bonus_multiplier=1.2):
        tokens = round(amount_eth * token_rate, 2)
        return round(tokens * bonus_multiplier, 2)

    @staticmethod
    def create_purchase_payload(wallet, eth_address, amount_eth, total_tokens):
        return {
            'wallet': wallet,
            'eth_address': eth_address,
            'amount_eth': amount_eth,
            'tokens_allocated': total_tokens,
        }