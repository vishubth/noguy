import sqlite3


def get_db(database_name='presale.db'):
    conn = sqlite3.connect(database_name)
    conn.row_factory = sqlite3.Row
    return conn


def init_database(database_name='presale.db'):
    conn = get_db(database_name)
    conn.execute('''
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
    ''')
    conn.commit()
    conn.close()