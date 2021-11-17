import binascii
from decimal import Decimal
from jumpscale.tools.servicemanager.servicemanager import BackgroundService
from jumpscale.packages.gettft.models.user_model import UserModel, users
from jumpscale.loader import j
from jumpscale.packages.gettft.bottle.shop import electrum
from jumpscale.packages.gettft.bottle.blockstream import BlockStream
from jumpscale.packages.gettft.sals.gettft_sals import get_tft_price
from jumpscale.packages.gettft.bottle.shop import XLM_WALLET_NAME

MAIL_QUEUE = "MAIL_QUEUE"


class XLMTransactionChecker(BackgroundService):
    def __init__(self, interval=10 * 60, *args, **kwargs):
        """10mins  (10 * 60)"""
        super().__init__(interval=interval, *args, **kwargs)
        self.TFT_WALLET = j.clients.stellar.get("tftshop_wallet")
        self.XLM_WALLET = j.clients.stellar.get(XLM_WALLET_NAME)

    def job(self):
        print("XLM Transaction checker")

        # Load price from github
        _, price = get_tft_price()

        # save xlm transactions
        xlm_transactions = {}

        # Switch array into hashmap for fast looking up O(1)
        stellar_transactions = {}

        # only get xlm transaction with amount > 0 to avoid spams
        for transaction in self.XLM_WALLET.list_transactions():
            if self.XLM_WALLET.check_is_payment_transaction(transaction.hash):
                tx_effects = self.XLM_WALLET.get_transaction_effects(transaction.hash)[0]
                if tx_effects.asset_code == "XLM" and tx_effects.amount > 0:
                    xlm_transactions[transaction.hash] = {
                        "memo_text": transaction.memo_text,
                        "amount": tx_effects.amount,
                    }

        # check paid transactions
        for transaction in self.TFT_WALLET.list_transactions():
            memo_hash = transaction.memo_hash_as_hex
            if (
                self.TFT_WALLET.address == self.TFT_WALLET.get_sender_wallet_address(transaction.hash)
                and type(memo_hash) is str
            ):
                stellar_transactions[memo_hash] = True

        for user_id in users.list_all():
            user = users.get(user_id)
            memo_text = user.memo_text
            for tx, tx_details in xlm_transactions.items():
                # if no memo text in the transaction, skip it
                if tx_details["memo_text"] != memo_text:
                    continue

                # If txid exists in stellar_transactions that's mean we already sent user back his tft
                if tx in stellar_transactions:
                    continue

                amount = tx_details["amount"]

                # save the user transaction price and use it later
                if user.transactions.find(f"tx_{tx}"):
                    user_transactions = user.transactions.get(f"tx_{tx}")
                else:
                    user_transactions = user.transactions.get(f"tx_{tx}")
                    user_transactions.tft_price = str(price)

                tft_amount = amount * Decimal(user_transactions.tft_price)  # Factor
                user_transactions.tft_amount = str(tft_amount)
                user_transactions.save()
                user.save()
                # add btc memo hash to stellar transaction
                tx_hash = binascii.unhexlify(tx)
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


service = XLMTransactionChecker()
