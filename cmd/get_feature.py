import requests
import csv
import pandas as pd

time_frame = 'TIME_SERIES_DAILY'
interval = 'daily'
symbol = 'DJI'
data_type = 'csv'
api_key = 'WJL5RGO2JQXHOO7Z'
indicator = 'RSI'
time_period = 8

url = 'https://www.alphavantage.co/query?function=' + time_frame + '&symbol=' + symbol + '&apikey=' + api_key + '&datatype=' + data_type + '&outputsize=full'
indicator_url = 'https://www.alphavantage.co/query?function=' + indicator + '&symbol=' + symbol + '&interval=' + interval + '&time_period=' + str(
    time_period) + '&series_type=open&apikey=' + api_key + '&datatype=' + data_type + '&outputsize=full'


def get_data(url: str):
    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        csv_file = list(cr)
        headers = csv_file[0]
        rows = csv_file[1:]
        data = pd.DataFrame(rows, columns=headers)
    return data


stock_prices = get_data(url)
stock_prices = stock_prices.rename(columns={"timestamp": "time"})
stock_indicators = get_data(indicator_url)
stock_data: pd.DataFrame = pd.concat([stock_prices, stock_indicators], axis=1, join='inner')
stock_data.to_csv('data/stock_data.csv', encoding='utf-8', sep=',', index=False)