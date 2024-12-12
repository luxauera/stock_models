from statsforecast.models import AutoARIMA
from statsforecast import StatsForecast
import pandas as pd
from assets.PostgresManager import PostgresModel
from datetime import datetime

 
class ARIMAModel(PostgresModel):
    def __init__(self, schema, table_name, end_date=None, target_column="Adj Close",seasonal=None):
        super().__init__()
        self.schema = schema
        self.table_name = table_name
        self.target_column = target_column
        self.seasonal = seasonal
        self.query = rf"""SELECT * FROM {self.schema}."{self.table_name}";"""
        self.end_date = end_date
        self.data = self.fetch_data()
        self.train_data = self.generate_train_data()
        self.predicted_price = self.predict_price()
        self.last_price = self.data[self.target_column].iloc[-1]
        self.model_date = datetime.now()
        self.data_max_date = self.data.index.max()

    
    def generate_train_data(self):
        data = self.data.copy()
        data['ds'] = data.index
        data['y'] = data[self.target_column]  
        data['unique_id'] = 1  
        return data[['unique_id', 'ds', 'y']]

    
    def fetch_data(self):
        if self.end_date is not None:
            data = pd.read_sql(self.query, self.engine)
            data = data[data['Date'] <= self.end_date]
        else:
            data = pd.read_sql(self.query, self.engine)
        return data.set_index('Date')
    
    def predict_price(self):
        auto_arima_model = AutoARIMA(seasonal=self.seasonal)
        forecast = StatsForecast(models=[auto_arima_model] , freq='D')
        forecast.fit(self.train_data)
        forecasted_values = forecast.predict(h=1)  # 1 adım tahmin
        return forecasted_values['AutoARIMA'].values[0]


