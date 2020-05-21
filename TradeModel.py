import endpoints
import pandas as pd
import plotly.graph_objs as go
import requests
import json

from plotly.offline import plot
from price_channel import PriceChennel


class TradeModel:
    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval
        self.df = self.get_data()

    def get_data(self):
        url = endpoints.BASE + \
              endpoints.KLINES + \
              endpoints.KLINE_PARAM.format(self.symbol, self.interval)

        data = requests.get(url)
        dictionary = json.loads(data.text)

        column_names = ["time", "open", "high", "low", "close", "volume"]
        df = pd.DataFrame.from_dict(dictionary)
        df.drop(columns=range(6, 12), inplace=True)
        df.columns = column_names

        for column in column_names:
            df[column] = df[column].astype(float)

        return df

    def plot_data(self):
        df = self.df

        kline = go.Candlestick(
            name="Candlestick",
            x=df['time'],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"]
        )

        pc_upper = go.Scatter(
            x=df['time'],
            y=df['pc_upper'],
            line_shape='linear',
            name="Price Channel(Upper)"
        )

        pc_lower = go.Scatter(
            x=df['time'],
            y=df['pc_lower'],
            line_shape='linear',
            name="Price Channel(Lower)"
        )

        data = [kline, pc_upper, pc_lower]
        layout = go.Layout(title="Symbol:{}. Time frame:{}".format(self.symbol, self.interval))
        fig = go.Figure(data=data, layout=layout)

        plot(fig, filename=self.symbol)

    def get_price_channel(self):
        df = self.df

        pc = PriceChennel(df['high'].tolist(), df['low'].tolist(), 20)

        df['pc_upper'] = pc.upper_channel()
        df['pc_lower'] = pc.lower_channel()


if __name__ == '__main__':
    model = TradeModel("BTCUSDT", "15m")
    model.get_price_channel()
    model.plot_data()
