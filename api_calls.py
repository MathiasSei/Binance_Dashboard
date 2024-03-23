import requests

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



base_url = "https://api.binance.com" #The URL of the Binance API

#Gets the server time from the Binance API
def get_server_time():
    url = base_url + "/api/v3/time"
    response = requests.get(url)
    return response.json()
