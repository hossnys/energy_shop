from datetime import datetime

from jumpscale.core.base import Base, StoredFactory, fields
from jumpscale.loader import j


class Transactions(Base):
    tft_price = fields.String()
    tft_amount = fields.String()
    date = fields.DateTime(default=datetime.utcnow)


class UserModel(Base):
    tft_address = fields.String()
    btc_address = fields.String()
    has_agreed = fields.Boolean(False)
    email = fields.String(default="")
    transactions = fields.Factory(Transactions)
    memo_text = fields.String(default=j.data.idgenerator.chars(28))

    @staticmethod
    def prefix(id: int):
        return f"USER_{id}"


users = StoredFactory(UserModel)
