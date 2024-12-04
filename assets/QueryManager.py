import pandas as pd
from assets.PostgresManager import PostgresModel


class QueryModel(PostgresModel):
    def __init__(self):
        super().__init__()
        self.query = """
        SELECT table_schema, 
               table_name
        FROM information_schema.tables
        WHERE table_schema = '{}'
          AND table_type = 'BASE TABLE';
        """
        self.ticker_tables_df = self.Fetch_Schema_Tables('tickers')
        self.clear_table_list = self.Create_Clear_Table_List()
        self.sub_tables_dict = self.Fetch_Sub_Tables()

    def Fetch_Schema_Tables(self, schema_name):
        return pd.read_sql_query(self.query.format(schema_name), self.engine)

    def Create_Clear_Table_List(self):
        def filter_func(x): return x != None
        temp_list = [
            None if 'utils' in x else x for x in self.ticker_tables_df["table_name"].values]
        return list(filter(filter_func, temp_list))

    def Fetch_Sub_Tables(self):
        temp_dict = {}
        for schema in self.clear_table_list:
            temp_dict[schema] = list(
                (self.Fetch_Schema_Tables(schema)["table_name"].values))
        return temp_dict
