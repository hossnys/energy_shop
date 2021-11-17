import datetime as dt
from decimal import Decimal

import requests
from jumpscale.loader import j

TFTPRICE_URL = "https://threefoldfoundation.github.io/tft-price/tftprice.json"
LIMITS_FILE_PATH = j.sals.fs.join_paths(j.sals.fs.parents(j.packages.gettft.sals.__file__)[1], "limits.json")


def get_limits():
    return j.data.serializers.json.load_from_file(LIMITS_FILE_PATH)


def calc_left_time():
    now = dt.datetime.now()
    res = (60 - now.minute) * 60 + (60 - now.second)
    if now.hour < 16:
        return res + (16 - now.hour - 1) * 3600
    return res + (24 - now.hour + 15) * 3600


def get_tft_price():
    btc_price = j.core.db.get("BTC_PRICE")
    xlm_price = j.core.db.get("XLM_PRICE")
    if all([btc_price, xlm_price]):
        return Decimal(btc_price.decode()), Decimal(xlm_price.decode())

    res = requests.get(TFTPRICE_URL)
    if res.status_code == 200:
        btc_price, xlm_price = Decimal(res.json().get("btc")), Decimal(res.json().get("xlm"))
        ex = calc_left_time()
        j.core.db.set("BTC_PRICE", str(btc_price), ex=ex)
        j.core.db.set("XLM_PRICE", str(xlm_price), ex=ex)
        return btc_price, xlm_price
    raise Exception("Couldn't fetch tft prices.")
