# src/db.py
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import os

# Load environment variables from .env file
load_dotenv()

# Read database configuration from environment variables
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# Create a SQLAlchemy connection URL
connection_string = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Create the SQLAlchemy engine
try:
    engine = create_engine(connection_string)
    with engine.connect() as connection:
        print("Database connection established successfully.")
except Exception as e:
    print(f"Error connecting to the database: {e}")

def get_data_from_mysql():
    """
    Fetch data from MySQL database and return as pandas DataFrame
    """
    try:
        query = "SELECT * FROM network_logs"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
