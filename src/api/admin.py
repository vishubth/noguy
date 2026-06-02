class AdminApi:

    @staticmethod
    def login_logic(username, password, admin_key, admin_password, token_generator, sessions):
        if username != admin_key or password != admin_password:
            raise ValueError('Invalid credentials')

        token = token_generator()
        sessions[token] = True
        return {'token': token}

    @staticmethod
    def purchases_logic(rows):
        return [dict(row) for row in rows]

    @staticmethod
    def stats_logic(total_transactions, confirmed, total_eth, total_tokens):
        return {
            'total_transactions': total_transactions,
            'confirmed': confirmed,
            'total_eth_received': round(total_eth or 0, 4),
            'total_tokens_allocated': total_tokens or 0,
        }
