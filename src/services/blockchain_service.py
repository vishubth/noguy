import requests

class BlockchainService:

    @staticmethod
    def get_live_usd_to_eth():
        try:
            res = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT', timeout=10)
            res.raise_for_status()
            eth_usd = float(res.json()['price'])
        except Exception:
            try:
                res = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot', timeout=10)
                res.raise_for_status()
                eth_usd = float(res.json()['data']['amount'])
            except Exception:
                return 0.00052

        return round(1 / eth_usd, 8)

    @staticmethod
    def verify_transaction(tx_hash, expected_wallet, expected_amount_eth, etherscan_api_key):
        try:
            params = {
                'module': 'transaction',
                'action': 'gettxreceiptstatus',
                'txhash': tx_hash,
                'apikey': etherscan_api_key
            }

            res = requests.get('https://api.etherscan.io/api', params=params, timeout=10).json()

            if res.get('status') != '1':
                return False

            tx_params = {
                'module': 'proxy',
                'action': 'eth_getTransactionByHash',
                'txhash': tx_hash,
                'apikey': etherscan_api_key
            }

            tx_data = requests.get('https://api.etherscan.io/api', params=tx_params, timeout=10).json()
            tx = tx_data.get('result')

            if not tx:
                return False

            to_address = tx.get('to', '').lower()

            if to_address != expected_wallet.lower():
                return False

            value_wei = int(tx.get('value', '0x0'), 16)
            value_eth = value_wei / 1e18

            return value_eth >= expected_amount_eth * 0.95

        except Exception:
            return False