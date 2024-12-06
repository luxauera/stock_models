import psycopg2
import os
from sqlalchemy import create_engine, Column, String, Date, MetaData, Integer, Float, text
from sqlalchemy.orm import sessionmaker
import pandas as pd



class PostgresModel:
    def __init__(self):
        self.DB_NAME = 'hcap' #os.environ['DB_NAME']
        self.DB_USER = 'postgres' #os.environ['DB_USER']
        self.DB_PASSWORD = 'mysecretpassword' #os.environ['DB_PASSWORD']
        self.DB_PORT = 5432 #os.environ['DB_PORT']
        self.DB_HOST = 'main-desktop' #os.environ['DB_HOST']

        self.engine = create_engine(
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.create_schema("logs")

    def test_connection(self):
        try:
            pd.read_sql_query("SELECT current_user;", self.engine)
            print("Database connection successful.")
            return True

        except Exception as e:
            print("Database connection failed:", e)
            return False

    def create_schema(self, schema_name):
        try:
            with self.engine.connect() as connection:
                connection.execute(
                    text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};"))
                connection.commit()
        except Exception as e:
            print(f"Failed to create schema '{schema_name}':", e)