class AllocationService:
    @staticmethod
    def calculate_allocation(amount_eth, token_rate, bonus=1.2):
        tokens = amount_eth * token_rate
        return round(tokens * bonus, 2)