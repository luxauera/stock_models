import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import tensorflow
from datetime import date
from datetime import timedelta
from datetime import datetime
from assets.PostgresManager import PostgresModel


class LSTMModeller(PostgresModel):
    def __init__(self, schema, table_name, target_column=["Adj Close"], end_date=None, lookback=60):
        super().__init__()
        self.target_column = target_column
        self.end_date = end_date
        self.lookback = lookback
        self.schema = schema
        self.table_name = table_name
        self.query = rf"""SELECT * FROM {self.schema}."{self.table_name}";"""
        self.data = pd.read_sql(self.query, self.engine)
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = self.create_model()
        self.predicted_price = self.predict_price()
        self.last_price = self.data[self.target_column].iloc[-1]
        self.predicted_price = self.predict_price()

    def create_model(self):
        data = self.data[self.target_column].values.reshape(-1, 1)
        data = self.scaler.fit_transform(data)
        x, y = [], []
        for i in range(self.lookback, len(data)):
            x.append(data[i - self.lookback:i, 0])
            y.append(data[i, 0])
        x, y = np.array(x), np.array(y)
        x = np.reshape(x, (x.shape[0], x.shape[1], 1))
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True,
                  input_shape=(x.shape[1], 1)))
        model.add(LSTM(units=50))
        model.add(Dense(units=1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x, y, epochs=1, batch_size=1, verbose=2)
        return model

    def predict_price(self):
        data = self.data[self.target_column].values.reshape(-1, 1)
        data = self.scaler.fit_transform(data)
        inputs = data[-self.lookback:]
        inputs = np.reshape(inputs, (1, inputs.shape[0], 1))
        predicted_price = self.scaler.inverse_transform(
            self.model.predict(inputs))
        return predicted_price[0][0]
