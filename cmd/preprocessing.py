import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np


def preprocess_data(file: str):
    stock_data = pd.read_csv(file, encoding='utf-8')
    stock_data['open_high'] = stock_data.apply(lambda row: compute_percentage_increase(row['open'], row['high']),
                                               axis=1)
    stock_data['open_low'] = stock_data.apply(lambda row: compute_percentage_increase(row['open'], row['low']), axis=1)
    stock_data['open_close'] = stock_data.apply(lambda row: compute_percentage_increase(row['open'], row['close']),
                                                axis=1)
    stock_data = drop_attribute(stock_data, ['time.1', 'time', 'open', 'close', 'high', 'low', 'volume'])
    stock_data['RSI'] = pd.DataFrame(stats.zscore(stock_data['RSI'].values))
    stock_data['color'] = compute_colors(stock_data['open_close'])
    stock_data = stock_data.iloc[1:]
    print(stock_data['RSI'].head(30))
    plt.hist(stock_data['open_high'].values, bins=100)
    plt.ylabel('freq')
    plt.show()
    stock_data.to_csv('data/stock_data_features.csv', encoding='utf-8', sep=',', index=False)


def drop_attribute(data: pd.DataFrame, columns: list) -> pd.DataFrame:
    return data.drop(columns=columns)


def compute_percentage_increase(start_price: float, target_price: float) -> float:
    return (target_price - start_price) / abs(start_price)


def compute_colors(data: pd.DataFrame) -> pd.DataFrame:
    data_list = np.array(data.values)
    data_list = np.roll(data_list, 1)
    color_func = np.vectorize(get_color)
    return pd.DataFrame(color_func(data_list))


def get_color(increase):
    if increase > 0:
        return 1
    return 0


preprocess_data('data/stock_data.csv')
