import datetime
import time
import pandas as pd
from core.env import require_env
from core.exceptions import AtfError
from trader.broker_apis.xtb import APIClient, login_command, base_command


def get_data(amount, interval, start_date):
    login = require_env("XTB_LOGIN")
    password = require_env("XTB_PASSWORD")
    client = APIClient()
    res = client.execute(login_command(user_id=login, password=password))
    if not res["status"]:
        raise AtfError(f"Login failed. Error code: {res['errorCode']}")

    res = client.execute(base_command("getChartLastRequest", info=dict(
        period=1,
        start=(time.time() - int(amount) * 60) * 1000,
        symbol="US500"
    )))

    if not res["status"]:
        raise AtfError(f"Getting chart data failed with error code {res['errorCode']}")

    rate_infos = res["returnData"]["rateInfos"]
    digits = res["returnData"]["digits"]

    opens = [record["open"] for record in rate_infos]
    dates = [record["ctm"] for record in rate_infos]
    highs = [open_price + record["high"] for record, open_price in zip(rate_infos, opens)]
    lows = [open_price + record["low"] for record, open_price in zip(rate_infos, opens)]
    closes = [open_price + record["close"] for record, open_price in zip(rate_infos, opens)]
    volumes = [record["vol"] for record in rate_infos]

    df = pd.DataFrame(data=dict(
        Open=[price / (10 ** digits) for price in opens],
        High=[price / (10 ** digits) for price in highs],
        Low=[price / (10 ** digits) for price in lows],
        Close=[price / (10 ** digits) for price in closes],
        Volume=volumes
    ), index=pd.DatetimeIndex([datetime.datetime.fromtimestamp(date / 1000) for date in dates]))

    client.disconnect()

    return df
