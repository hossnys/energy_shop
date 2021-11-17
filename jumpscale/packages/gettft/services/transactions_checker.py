import binascii
from decimal import Decimal
from jumpscale.tools.servicemanager.servicemanager import BackgroundService
from jumpscale.packages.gettft.models.user_model import UserModel, users
from jumpscale.loader import j
from jumpscale.packages.gettft.bottle.shop import electrum
from jumpscale.packages.gettft.bottle.blockstream import BlockStream
from jumpscale.packages.gettft.sals.gettft_sals import get_tft_price

MAIL_QUEUE = "MAIL_QUEUE"


class TransactionsChecker(BackgroundService):
    def __init__(self, interval=10 * 60, *args, **kwargs):
        """10mins  (10 * 60)"""
        super().__init__(interval=interval, *args, **kwargs)
        self.TFT_WALLET = j.clients.stellar.get("tftshop_wallet")
        self.API = BlockStream(electrum.test_net)

    def job(self):
        print("Transaction checker")

        # Load price from github
        price, _ = get_tft_price()

        """Switch array into hashmap for fast looking up O(1)"""
        stellar_transactions = {}
        for transaction in self.TFT_WALLET.list_transactions():
            memo_hash = transaction.memo_hash_as_hex
            if (
                self.TFT_WALLET.address == self.TFT_WALLET.get_sender_wallet_address(transaction.hash)
                and type(memo_hash) is str
            ):
                stellar_transactions[memo_hash] = True

        for id in users.list_all():
            user: UserModel = users.find(id)

            txs = self.API.list_transactions(user.btc_address)

            for tx in txs:
                txid = tx.get("txid")

                """If txid exists in stellar_transactions that's mean we already sent user back his tft"""
                if txid in stellar_transactions:
                    continue

                amount = BlockStream.get_amount(tx, user.btc_address)
                if amount == 0:
                    continue

                # get transaction confirmation status, if not confirmed skip this transaction
                is_confirmed_tx = tx["status"]["confirmed"]
                if not is_confirmed_tx:
                    continue

                # save the user transaction price and use it later
                if user.transactions.find(f"tx_{txid}"):
                    user_transactions = user.transactions.get(f"tx_{txid}")
                else:
                    user_transactions = user.transactions.get(f"tx_{txid}")
                    user_transactions.tft_price = str(price)

                tft_amount = amount * Decimal(user_transactions.tft_price)  # Factor
                user_transactions.tft_amount = str(tft_amount)
                user_transactions.save()
                user.save()
                # add btc memo hash to stellar transaction
                tx_hash = binascii.unhexlify(txid)
                try:
                    tx_hash = self.TFT_WALLET.transfer(
                        destination_address=user.tft_address,
                        amount=str(tft_amount.to_integral_value()),
                        asset=f"{self.TFT_WALLET._get_asset('TFT').code}:{self.TFT_WALLET._get_asset('TFT').issuer}",
                        memo_hash=tx_hash,
                    )
                    mail_info = {
                        "recipients_emails": [user.email],
                        "sender": "no-reply@gettft.com",
                        "subject": "Get TFT transaction details",
                        "message": f"Congratulations\nWe have transferred {tft_amount} TFT to your address:{user.tft_address}\nWith transaction hash:{tx_hash}\nThanks for using Get TFT",
                    }
                    j.core.db.rpush(MAIL_QUEUE, j.data.serializers.json.dumps(mail_info))

                except Exception as e:
                    j.logger.error(f"Transaction checker Error, failed to make transaction due to {e}")


service = TransactionsChecker()
