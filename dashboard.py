from flask import Flask, render_template
import api_calls

app = Flask(__name__)

@app.route('/')
def index():

    btcPrice = api_calls.get_btc_price()
    totalValue = api_calls.get_total_assets_in_USDT()["Total"]

    return render_template('index.html', 
                           btcPrice = btcPrice,
                           totalValue = totalValue,
                           totalBTCValue = round(totalValue / btcPrice, 5)
                           )

if __name__ == '__main__':
    app.run()