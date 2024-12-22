from assets.PostgresManager import PostgresModel
from assets.QueryManager import QueryModel
from assets.Statics import Stock_Stats
from assets.GARCHModel import GarchModel
from assets.SARIMAModel import ARIMAModel
from assets.LYAPONOVModel import LyapunovModel
import time
import os
from datetime import datetime
import pandas as pd


dbmodel = PostgresModel()
querymodel = QueryModel()


def Garch_Process():
    for schema in querymodel.sub_tables_dict.keys():
        created_schema_name = "garch" + schema
        dbmodel.create_schema(created_schema_name)
        for table in querymodel.sub_tables_dict[schema]:
            try:
                GARCH = GarchModel(schema=schema, table_name=table)
                values = [GARCH.table_name, GARCH.predicted_price,GARCH.last_price, GARCH.model_date, GARCH.data_max_date , GARCH.weekly_predicted_price, GARCH.weekly_last_price, GARCH.monthly_predicted_price, GARCH.monthly_last_price]
                columns = ["table_name", "predicted_price", "last_price", "model_date", "data_max_date" , "weekly_predicted_price", "weekly_last_price", "monthly_predicted_price", "monthly_last_price"]
                df = pd.DataFrame([values], columns=columns)
                df.to_sql(table, con=dbmodel.engine, schema=created_schema_name, if_exists="append", index=False)
            except Exception as e:
                print(e)

def Stats_Process():
    for schema in querymodel.sub_tables_dict.keys():
        created_schema_name = "stats" + schema
        dbmodel.create_schema(created_schema_name)
        for table in querymodel.sub_tables_dict[schema]:
            try:
                STATS = Stock_Stats(schema=schema, table_name=table)
                values = [STATS.table_name, STATS.last_price , STATS.former_price ,STATS.mean_pct,STATS.std_pct, STATS.price_return, STATS.data_max_date]
                columns = ["table_name","last_price" ,"former_price" , "mean", "std", "return", "data_max_date"]
                df = pd.DataFrame([values], columns=columns)
                df.to_sql(table, con=dbmodel.engine, schema=created_schema_name, if_exists="append", index=False)
            except Exception as e:
                print(e)


def Sarima_Process():
    for schema in querymodel.sub_tables_dict.keys():
        created_schema_name = "arima" + schema
        dbmodel.create_schema(created_schema_name)
        for table in querymodel.sub_tables_dict[schema]:
            try:
                ARIMA = ARIMAModel(schema=schema, table_name=table)
                values = [ARIMA.table_name, ARIMA.predicted_price,ARIMA.last_price, ARIMA.model_date, ARIMA.data_max_date , ARIMA.weekly_predicted_price, ARIMA.weekly_last_price, ARIMA.monthly_predicted_price, ARIMA.monthly_last_price]
                columns = ["table_name", "predicted_price", "last_price", "model_date", "data_max_date", "weekly_predicted_price", "weekly_last_price", "monthly_predicted_price", "monthly_last_price"]
                df = pd.DataFrame([values], columns=columns)
                df.to_sql(table, con=dbmodel.engine, schema=created_schema_name, if_exists="append", index=False)
            except Exception as e:
                print(e)

def Lyaponob_Process():
    for schema in querymodel.sub_tables_dict.keys():
        created_schema_name = "lyapunov" + schema
        dbmodel.create_schema(created_schema_name)
        for table in querymodel.sub_tables_dict[schema]:
            try:
                LYAPONOV = LyapunovModel(schema=schema, table_name=table)
                values = [LYAPONOV.table_name, LYAPONOV.predicted_price,LYAPONOV.last_price, LYAPONOV.model_date, LYAPONOV.data_max_date , LYAPONOV.weekly_predicted_price, LYAPONOV.weekly_last_price, LYAPONOV.monthly_predicted_price, LYAPONOV.monthly_last_price]
                columns = ["table_name", "predicted_price", "last_price", "model_date", "data_max_date", "weekly_predicted_price", "weekly_last_price", "monthly_predicted_price", "monthly_last_price"]
                df = pd.DataFrame([values], columns=columns)
                df.to_sql(table, con=dbmodel.engine, schema=created_schema_name, if_exists="append", index=False)
            except Exception as e:
                print(e)


def Model_Process():
    while True:
        hour = datetime.now().strftime("%H:%M")
        print("Model Process is running " , hour)
        time.sleep(1)
        if hour == os.environ["RUN_PERIOD"]:
            print("Model Process is initiated")
            Garch_Process()
            Stats_Process()
            Sarima_Process()
            Lyaponob_Process()
            print("Model Process is completed")





if __name__ == "__main__":
    Model_Process()
else:
    pass


