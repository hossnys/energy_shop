from decimal import Decimal
import os

from jumpscale.loader import j
from jumpscale.packages.auth.bottle.auth import get_user_info
from jumpscale.packages.gettft.bottle.electrum import Electrum
from jumpscale.packages.gettft.models.user_model import UserModel, users
from jumpscale.packages.gettft.sals.gettft_sals import get_limits

from bottle import Bottle, HTTPResponse, request

app = Bottle()
is_testnet = os.environ.get("network") == "testnet"
electrum = Electrum(j.core.config.get("tftshop_mpk"), is_testnet)
XLM_WALLET_NAME = "gettft_xlm"


def _get_user_info(key):
    return j.data.serializers.json.loads(get_user_info()).get(key)


@app.route("/api/address", method="GET")
def get_address_handler():
    id = UserModel.prefix(_get_user_info("tid"))
    user = users.find(id)
    xlm_wallet = j.clients.stellar.get(XLM_WALLET_NAME)
    if user:
        return HTTPResponse(
            j.data.serializers.json.dumps(
                {
                    "tft_address": _get_user_info("walletAddress"),
                    "btc_address": user.btc_address,
                    "xlm_address": xlm_wallet.address,
                    "memo_text": user.memo_text,
                }
            ),
            status=200,
            headers={"Content-Type": "application/json"},
        )

    return HTTPResponse(
        j.data.serializers.json.dumps({"message": "User not found."}),
        status=404,
        headers={"Content-Type": "application/json"},
    )


@app.route("/api/accept", method="GET")
def accept_handler():
    id = UserModel.prefix(_get_user_info("tid"))

    user: UserModel = users.find(id)
    """ Create new user entry if not found (first time to visit site) """
    user_info = j.data.serializers.json.loads(get_user_info())
    email = user_info["email"]
    if user is None:
        user = users.new(id)
        user.tft_address = ""
        user.btc_address = electrum.create_address()
        user.has_agreed = False
        user.email = email

    if user.has_agreed:
        return HTTPResponse(
            j.data.serializers.json.dumps({"allowed": True}), status=200, headers={"Content-Type": "application/json"}
        )

    user.has_agreed = True
    user.save()
    return HTTPResponse(
        j.data.serializers.json.dumps({"allowed": True}), status=201, headers={"Content-Type": "application/json"}
    )


@app.route("/api/allowed", method="GET")
def allowed_handler():
    id = UserModel.prefix(_get_user_info("tid"))
    user: UserModel = users.find(id)
    result = user is not None and user.has_agreed

    return HTTPResponse(
        j.data.serializers.json.dumps({"allowed": result}), status=200, headers={"Content-Type": "application/json"}
    )


@app.route("/api/payment", method="POST")
def add_address_handler():
    address: str = request.json.get("address")
    amount: str = request.json.get("amount")
    limit_per_time = int(Decimal(get_limits()["limit_per_time"]).to_integral_value())

    if int(amount) > limit_per_time:
        return HTTPResponse(
            j.data.serializers.json.dumps(
                {"message": f"Error: Requested amount exceeded the limit of {limit_per_time} TFT per time"}
            ),
            status=403,
            headers={"Content-Type": "application/json"},
        )
    if type(address) is not str or not address.startswith("G") or len(address) != 56:
        return HTTPResponse(
            j.data.serializers.json.dumps(
                {
                    "message": "Address is not valid Should (startwith G and contains 56 chars).",
                }
            ),
            status=400,
            headers={"Content-Type": "application/json"},
        )

    id = _get_user_info("tid")

    try:
        j.clients.stellar.get("tftshop_wallet").get_balance(address)
        user = users.find(UserModel.prefix(id))
        if user:
            user.tft_address = address
        else:
            user = users.new(UserModel.prefix(id))
            user.tft_address = address
            user.btc_address = electrum.create_address()
        user.save()

        # make sure user didn't exceed the limit per day
        transactions = user.transactions.list_all()
        today = j.data.time.utcnow().date().day
        total_today_tft = 0
        limit_per_day = int(Decimal(get_limits()["limit_per_day"]).to_integral_value())

        for tx in transactions:
            trans = user.transactions.get(tx)
            if trans.date.day == today:
                total_today_tft += int(Decimal(trans.tft_amount).to_integral_value())

        if total_today_tft >= limit_per_day:
            return HTTPResponse(
                j.data.serializers.json.dumps(
                    {"message": f"Error: Exceeded the daily limit of {limit_per_day} TFT, Please try again tomorrow"}
                ),
                status=403,
                headers={"Content-Type": "application/json"},
            )
        return HTTPResponse(
            j.data.serializers.json.dumps({"tft_address": user.tft_address, "btc_address": user.btc_address}),
            status=200,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        j.logger.exception("error", exception=e)
        return HTTPResponse(
            j.data.serializers.json.dumps(
                {
                    "message": "Address is not valid.",
                }
            ),
            status=400,
            headers={"Content-Type": "application/json"},
        )
