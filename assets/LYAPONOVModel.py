import pandas as pd
from scipy.integrate import odeint
from assets.PostgresManager import PostgresModel
from warnings import filterwarnings
from datetime import datetime
import numpy as np
filterwarnings("ignore")

class LyapunovModel(PostgresModel):
    def __init__(self, schema, table_name, end_date=None, target_column="Adj Close"):
        super().__init__()
        self.schema = schema
        self.table_name = table_name
        self.target_column = target_column
        self.query = rf"""SELECT * FROM {self.schema}."{self.table_name}";"""
        self.end_date = end_date
        # Daily Calculations
        self.data = self.fetch_data()
        self.lyapunov_exp = self.calculate_lyapunov(self.data)
        self.predicted_price = self.predict_price(self.data, self.lyapunov_exp)
        self.last_price = self.data[self.target_column].iloc[-1]
        self.model_date = datetime.now()
        self.data_max_date = self.data.index.max()
        # Weekly Calculations
        self.weekly_data = self.data.to_period("W").groupby("Date").max()
        self.weekly_lyapunov_exp = self.calculate_lyapunov(self.weekly_data)
        self.weekly_predicted_price = self.predict_price(self.weekly_data, self.weekly_lyapunov_exp)
        self.weekly_last_price = self.weekly_data[self.target_column].iloc[-1]

        # Monthly Calculations
        self.monthly_data = self.data.to_period("M").groupby("Date").max()
        self.monthly_lyapunov_exp = self.calculate_lyapunov(self.monthly_data)
        self.monthly_predicted_price = self.predict_price(self.monthly_data, self.monthly_lyapunov_exp)
        self.monthly_last_price = self.monthly_data[self.target_column].iloc[-1]

    def fetch_data(self):
        if self.end_date is not None:
            data = pd.read_sql(self.query, self.engine)
            data = data[data['Date'] <= self.end_date]
        else:
            data = pd.read_sql(self.query, self.engine)
        return data.set_index('Date')

    def calculate_lyapunov(self, df):
        # Calculate returns
        returns = df[self.target_column].pct_change().dropna()
       
        # Define a simple dynamical system (e.g., logistic map)
        def logistic_map(x, r):
            return r * x * (1 - x)

        # Lyapunov exponent calculation
        r = 3.8  # Example parameter for chaotic behavior
        x0 = 0.5
        iterations = len(returns)
        lyapunov_sum = 0

        for _ in range(iterations):
            x1 = logistic_map(x0, r)
            derivative = abs(r * (1 - 2 * x0))
            if derivative == 0:
                derivative = 1e-10  # Prevent log(0)
            lyapunov_sum += np.log(derivative)
            x0 = x1

        return lyapunov_sum / iterations

    def predict_price(self, df, lyapunov_exp):
        # Use Lyapunov exponent to scale past returns for price prediction
        returns = df[self.target_column].pct_change().dropna()
        predicted_return = returns.mean() * (1 + lyapunov_exp)
        if not np.isfinite(predicted_return):
            predicted_return = 0  # Handle infinite or NaN returns
        predicted_price = df[self.target_column].iloc[-1] * (1 + predicted_return)
        return max(predicted_price, 0)  # Ensure non-negative price

