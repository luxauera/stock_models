
import pandas as pd
from arch import arch_model
from assets.PostgresManager import PostgresModel
from warnings import filterwarnings 
filterwarnings("ignore")


class GarchModel(PostgresModel):
    def __init__(self , schema , table_name , end_date=None, target_column = "Adj Close"):
        super().__init__()
        self.table_name = table_name
        self.schema = schema
        self.table_name = table_name
        self.target_column = target_column
        self.query = rf"""SELECT "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume" FROM {self.schema}."{self.table_name}";"""
        self.end_date = end_date
        self.data = self.fetch_data()
        self.predicted_price = self.predict_price()

    def fetch_data(self):
        if self.end_date is not None:
            data = pd.read_sql(self.query, self.engine)
            data = data[data['Date'] <= self.end_date]
        else:
            data = pd.read_sql(self.query, self.engine)
        return data.set_index('Date')

    def predict_price(self):
        returns = self.data[self.target_column].pct_change().dropna()
        model = arch_model(returns, vol='Garch', p=1, q=1)
        fitted_model = model.fit(disp='off')
        forecast = fitted_model.forecast(horizon=1, reindex=False)
        predicted_return = forecast.mean.iloc[-1, 0]
        predicted_variance = forecast.variance.iloc[-1, 0]
        predicted_price = self.data[self.target_column].iloc[-1] * (1 + predicted_return)
        return predicted_price

