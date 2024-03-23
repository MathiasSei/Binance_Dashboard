from flask import Flask, render_template
import api_calls

app = Flask(__name__)

@app.route('/')
def index():

    btcPrice = api_calls.get_btc_price()
    totalValue_coinValues = api_calls.get_total_assets_in_USDT()
    coin_data = [(coin, f"${round(value, 2)}") for coin, value in totalValue_coinValues[1].items() if coin in ["BTC", "USDT", "BNB"]]
    coin_data.reverse()

    return render_template('index.html', 
                           btcPrice = btcPrice,
                           totalValue = totalValue_coinValues[0]["Total"],
                           totalBTCValue = round(totalValue_coinValues[0]["Total"] / btcPrice, 5),
                           coin_data = coin_data
                           )

if __name__ == '__main__':
    app.run()