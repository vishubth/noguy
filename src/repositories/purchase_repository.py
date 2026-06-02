class PurchaseRepository:

    @staticmethod
    def create_purchase(conn, wallet, amount, amount_eth, tokens_allocated):
        conn.execute(
            '''
            INSERT INTO purchases (wallet, amount, amount_eth, tokens_allocated)
            VALUES (?, ?, ?, ?)
            ''',
            (wallet, amount, amount_eth, tokens_allocated),
        )
        conn.commit()

    @staticmethod
    def get_latest_purchase_by_wallet(conn, wallet):
        return conn.execute(
            'SELECT * FROM purchases WHERE wallet=? ORDER BY id DESC LIMIT 1',
            (wallet,),
        ).fetchone()

    @staticmethod
    def get_purchases_by_wallet(conn, wallet, include_unconfirmed=False):
        if include_unconfirmed:
            return conn.execute(
                '''
                SELECT id, wallet, amount, amount_eth, tokens_allocated,
                       tx_hash, confirmed, created_at
                FROM purchases
                WHERE wallet=?
                ORDER BY created_at DESC
                ''',
                (wallet,),
            ).fetchall()

        return conn.execute(
            '''
            SELECT id, wallet, amount, amount_eth, tokens_allocated,
                   tx_hash, confirmed, created_at
            FROM purchases
            WHERE wallet=? AND confirmed=1
            ORDER BY created_at DESC
            ''',
            (wallet,),
        ).fetchall()

    @staticmethod
    def confirm_purchase(conn, purchase_id, tx_hash):
        conn.execute(
            'UPDATE purchases SET confirmed=1, tx_hash=? WHERE id=?',
            (tx_hash, purchase_id),
        )
        conn.commit()

    @staticmethod
    def delete_purchase(conn, purchase_id):
        conn.execute('DELETE FROM purchases WHERE id=?', (purchase_id,))
        conn.commit()
