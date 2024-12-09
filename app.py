import pandas as pd
from assets.PostgresManager import PostgresModel
from assets.QueryManager import QueryModel
from assets.Statics import Stock_Stats
from assets.GARCHModel import GarchModel
import time
import os

dbmodel = PostgresModel()
querymodel = QueryModel()


def Garch_Process():
    for schema in querymodel.sub_tables_dict.keys():
        created_schema_name = "garch" + schema
        dbmodel.create_schema(created_schema_name)
        for table in querymodel.sub_tables_dict[schema]:
            try:
                GARCH = GarchModel(schema=schema, table_name=table)
                values = [GARCH.table_name, GARCH.predicted_price,GARCH.last_price, GARCH.model_date, GARCH.data_max_date]
                columns = ["table_name", "predicted_price", "last_price", "model_date", "data_max_date"]
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

def Model_Process():
    while True:
        time.sleep(int(os.environ["RUN_PERIOD"]))
        Garch_Process()
        Stats_Process()



if __name__ == "__main__":
    Model_Process()
else:
    pass