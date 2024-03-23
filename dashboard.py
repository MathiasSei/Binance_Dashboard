from flask import Flask, render_template
import api_calls

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', btcPrice = api_calls.get_btc_price())

if __name__ == '__main__':
    app.run()