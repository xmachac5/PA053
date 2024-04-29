import requests
from flask import Flask, request, Response

app = Flask(__name__)


@app.route("/")
def query():
    args = request.args
    if len(args) != 1:
        return Response(status=422)

    keys = args.keys()
    if 'queryAirportTemp' in keys:
        param = args.get('queryAirportTemp')
        query_result = airport_temperature(param)
    elif 'queryStockPrice' in keys:
        param = args.get('queryStockPrice')
        query_result = stock_price(param)
    elif 'queryEval' in keys:
        param = args.get('queryEval')
        query_result = calculate(param)
    else:
        return Response(status=422)

    try:
        result_value = float(query_result)
    except ValueError:
        return Response(status=500)

    return Response(str(result_value), mimetype='application/json', status=200)


def get_temperature(iata_code):
    url = f"http://api.weatherapi.com/v1/current.json?key=d6fe5f8a364a4d9bafe121634242904&q=iata:{iata_code}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temp_c']
        return temperature
    else:
        return None


def airport_temperature(param):
    temperature = get_temperature(param)
    if temperature:
        return temperature
    return None


def stock_price(param):
    headers = {
        'x-rapidapi-key': '1a94dbf958msh5abbb8f08b4527dp12f857jsn1df9c0205de4',
        'x-rapidapi-host': 'apidojo-yahoo-finance-v1.p.rapidapi.com'
    }
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary?symbol={param}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        current_price = data['price']['regularMarketPrice']['raw']
        return current_price
    return None


def calculate(param):
    try:
        response = eval(param)
        return response
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=41181, debug=True)
