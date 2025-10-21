# src/load_to_mysql.py
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# Create database connection
connection_string = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
engine = create_engine(connection_string)

# Read the cleaned CSV
df = pd.read_csv("telecom_network_logs_clean.csv")
print("Loaded cleaned data with shape:", df.shape)

# Define table name
table_name = "network_logs"

# Optional: Define MySQL schema (CREATE TABLE if not exists)
create_table_query = """
CREATE TABLE IF NOT EXISTS network_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp VARCHAR(50),
    region VARCHAR(50),
    device_id VARCHAR(50),
    customer_id VARCHAR(50),
    latency_ms FLOAT,
    uptime_percent FLOAT,
    packet_loss_rate FLOAT,
    bandwidth_usage_mb FLOAT
);
"""

# Execute table creation
with engine.connect() as conn:
    conn.execute(text(create_table_query))
    conn.commit()
    print("Table 'network_logs' is ready.")

# Load data into table
df.to_sql(table_name, con=engine, if_exists='append', index=False)
print("Data successfully inserted into MySQL table 'network_logs'!")
