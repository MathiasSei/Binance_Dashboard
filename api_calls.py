import hashlib
import hmac
import requests


import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start time before function execution
        result = func(*args, **kwargs)  # Function execution
        end_time = time.time()  # End time after function execution
        print(f"{func.__name__} took {end_time - start_time} seconds to run.")
        return result
    return wrapper

base_url = "https://api.binance.com" #The URL of the Binance API
trading_bot_assets = 781 #Edit this value manually



#Gets the API keys from the api_keys.txt file. Insert your keys in the file in the format:
# api_key=your_api_key          (No spaces)
# secret_key=your_api_secret    (No spaces)
def get_api_keys():
    file_path = "api_keys.txt" #Rename if your api_keys file is named differently
    api_keys = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            api_keys[key] = value
    headers = {
        "X-MBX-APIKEY": api_keys["api_key"],
        "X-API-SECRET": api_keys["secret_key"]
    }
    return api_keys["api_key"], api_keys["secret_key"], headers

#Gets the server time from the Binance API
def get_server_time():
    url = base_url + "/api/v3/time"
    response = requests.get(url)
    return response.json()

#Creates a signature for the request
def create_signature(api_secret, params=None):
    timestamp = get_server_time()["serverTime"]
    query_string = f"timestamp={timestamp}"
    if params:
        sorted_params = sorted(params.items())  # Sort parameters by key
        query_params = '&'.join([f"{k}={v}" for k, v in sorted_params])
        query_string += f"&{query_params}"  # Add parameters to query string
    hmac_obj = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256)
    timestamp_signature = f"?timestamp={timestamp}&signature={hmac_obj.hexdigest()}"
    return timestamp_signature

#Gets BTC/USDT price from the Binance API
def get_btc_price():
    url = base_url + "/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    return int(float(response.json()["price"])) #Converts the price to an integer

#Gets the user's assets from the Binance API
def get_spot_assets():
    spot_assets = {}
    api_key, api_secret, headers = get_api_keys()
    params = {"needBtcValuation": "true"}
    userAssets = f"/sapi/v3/asset/getUserAsset{create_signature(api_secret, params)}"
    url = base_url + userAssets
    response = requests.post(url, headers=headers, params=params).json()
    btc_price = get_btc_price()
    for i in response:
        if float(i["btcValuation"]) > 0:
            spot_assets[i["asset"]] = {"btcValuation": i["btcValuation"], "USDValuation": float(i["btcValuation"]) * btc_price}
    return spot_assets

#Gets assets in earn wallet
def get_earn_assets():
    earn_assets = {}
    api_key, api_secret, headers = get_api_keys()
    earn_assets_url = f"/sapi/v1/simple-earn/account{create_signature(api_secret)}"
    url = base_url + earn_assets_url
    response = requests.get(url, headers=headers).json()
    if float(response["totalFlexibleAmountInUSDT"]) > 0:
        url = base_url + f"/sapi/v1/simple-earn/flexible/position{create_signature(api_secret)}"
        flexible = requests.get(url, headers=headers).json()
        earn_assets["Flexible"] = []
        for i in flexible["rows"]:
            if float(i["totalAmount"]) > 0:
                earn_assets["Flexible"].append({"asset": i["asset"], "amount": i["totalAmount"]})
    elif float(response["totalLockedAmountInUSDT"]) > 0:
        url = base_url + f"/sapi/v1/simple-earn/locked/position{create_signature(api_secret)}"
        locked = requests.get(url, headers=headers).json()
        earn_assets["Locked"] = []
        for i in locked["rows"]:
            if float(i["totalAmount"]) > 0:
                earn_assets["Locked"].append({"asset": i["asset"], "amount": i["totalAmount"]})
    total_assets_value = 0
    for i in earn_assets:
        for j in earn_assets[i]:
            total_assets_value += float(j["amount"])
    return earn_assets, round(total_assets_value, 2)

#Gets the total assets in USDT
def get_total_assets_in_USDT():
    spot_assets = get_spot_assets()
    earn_assets, earn_assets_value = get_earn_assets()
    total_assets = {}
    coin_values = {}
    spot_value = 0
    for i in spot_assets:
        if i in ["BTC", "USDT", "BNB"]:
            coin_values[i] = float(spot_assets[i]["USDValuation"])
        spot_value += float(spot_assets[i]["USDValuation"])
    for i in earn_assets:
        for j in earn_assets[i]:
            if j["asset"] in ["BTC", "USDT", "BNB"]:
                coin_values[j["asset"]] = float(j["amount"])
    total_assets["Spot"] = spot_value
    total_assets["Earn"] = earn_assets_value
    total_assets["TradingBots"] = trading_bot_assets #API does not support trading bot assets, edit this value manually
    total_assets["Total"] = round(float(spot_value) + earn_assets_value + total_assets["TradingBots"], 2)
    return total_assets, coin_values

import urllib.parse

def get_all_trades():
    api_key, api_secret, headers = get_api_keys()
    params = {
        "symbol": "BTCUSDT",
        "startTime": 1704133438000,
        "timestamp": int(time.time() * 1000)  # Current timestamp in milliseconds
    }
    params = dict(sorted(params.items()))  # Sort parameters by key
    query_string = urllib.parse.urlencode(params)  # URL-encode parameters
    signature = hmac.new(bytes(api_secret , 'latin-1'), msg = bytes(query_string , 'latin-1'), digestmod = hashlib.sha256).hexdigest()
    params['signature'] = signature
    trades_url = "/api/v3/myTrades"
    url = base_url + trades_url
    response = requests.get(url, headers=headers, params=params).json()
    return response
