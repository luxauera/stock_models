import pandas as pd
import numpy as np
from assets.PostgresManager import PostgresModel

class Stock_Stats(PostgresModel):
    def __init__(self ,schema ,table_name,target_col="Adj Close",end_date=None):
        super().__init__()
        self.schema = schema
        self.table_name = table_name
        self.end_date = end_date
        self.query = rf"""SELECT * FROM {self.schema}."{self.table_name}";"""
        self.tdf = self.fetch_data()
        self.target_col = target_col
        self.ticker_data_lenght = len(self.tdf)
        self.series = self.tdf[self.target_col].values
        self.series_pct = self.tdf[self.target_col].pct_change().fillna(0).values
        self.data_max_date = self.tdf.index.max()
        self.last_price = self.series[-1]
        self.former_price = self.series[-2]
        # Stats
        self.mean = self.Calc_Mean(self.series)
        self.std = self.Calc_Std(self.series)
        self.var = self.Calc_Var(self.series)
        self.price_return = self.Calc_Return()

        self.mean_pct = self.Calc_Mean(self.series_pct)
        self.std_pct = self.Calc_Std(self.series_pct)
        self.var_pct = self.Calc_Var(self.series_pct)

    def fetch_data(self):
        if self.end_date is not None:
            data = pd.read_sql(self.query, self.engine)
            data = data[data['Date'] <= self.end_date]
        else:
            data = pd.read_sql(self.query, self.engine)
        return data.set_index('Date')
    
    def Calc_Mean(self , series):
        return float(np.mean(series))
    
    def Calc_Std(self , series):
        return float(np.std(series))
    
    def Calc_Var(self , series):
        return float(np.var(series))
    
    def Calc_Return(self):
        return (self.last_price - self.former_price) / self.former_price

