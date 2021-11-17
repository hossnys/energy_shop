import requests
from decimal import Decimal


class BlockStream:

    def __init__(self, test_net: bool):
        self.test_net = test_net
        suffix = "testnet/api" if self.test_net else "api"
        self.api = "https://blockstream.info/" + suffix

    def list_transactions(self, address: str) -> list:
        api = f"{self.api}/address/{address}/txs"
        res = requests.get(api)
        if res.status_code != 200:
            return []
        return res.json()

    @staticmethod
    def get_amount(tx, address: str) -> Decimal:
        for v in tx.get('vout'):
            if v.get('scriptpubkey_address') == address:
                return Decimal(v.get('value')) / Decimal(100000000)  # 1e8
        return Decimal(0)
