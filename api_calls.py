import hashlib
import hmac
import requests

base_url = "https://api.binance.com" #The URL of the Binance API

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
    return [api_keys["api_key"], api_keys["secret_key"]]

#Gets the server time from the Binance API
def get_server_time():
    url = base_url + "/api/v3/time"
    response = requests.get(url)
    return response.json()

#Creates a signature for the request
def create_signature(api_secret, timestamp):
    query_string = f"timestamp={timestamp}"
    hmac_obj = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256)
    return hmac_obj.hexdigest()

#Gets the user's assets from the Binance API
def get_user_assets():
    api_key, api_secret = get_api_keys()
    headers = {
        "X-MBX-APIKEY": api_key,
        "X-API-SECRET": api_secret
    }
    timestamp = get_server_time()["serverTime"]
    signature = create_signature(api_secret, timestamp)
    userAssets = f"/sapi/v3/asset/getUserAsset?timestamp={timestamp}&signature={signature}"
    url = base_url + userAssets
    response = requests.post(url, headers=headers)
    return response.json()

print(get_user_assets())