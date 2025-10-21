# src/pipeline.py
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

# Database connection
connection_string = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
engine = create_engine(connection_string)

print(" Starting Telecom Data Pipeline... ")

# -------------------
# Step 1. Extraction
# -------------------

try:
    df = pd.read_csv("data/telecom_network_logs_raw.csv")
    print("Raw data loaded successfully — shape:", df.shape)
except FileNotFoundError:
    print("Error: Raw data file not found.")
    exit(1)
    
# -------------------
# Step 2. Transformation (Cleaning)
# -------------------

df['region'] = df['region'].fillna('Unknown')
df['device_id'] = df['device_id'].fillna('Unknown')

if df['latency_ms'].isnull().any():
    df['latency_ms'] = df['latency_ms'].fillna(df['latency_ms'].mean())

df['packet_loss_rate'] = df['packet_loss_rate'].apply(lambda x: np.nan if x < 0 else x)
df['uptime_percent'] = df['uptime_percent'].apply(lambda x: np.nan if x < 0 or x > 100 else x)
df = df.fillna({'packet_loss_rate': 0.0, 'uptime_percent': 0.0, 'latency_ms': 0.0})

print("Data cleaned and trasnformed successfully — shape:", df.shape)

# -------------------
# Step 3. Load to MySQL
# -------------------

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

with engine.connect() as connection:
    connection.execute(text(create_table_query))
    connection.commit()
    
df.to_sql("network_logs", con=engine, if_exists="append", index=False)
print("Data loaded into MySQL database successfully!")

# -------------------
# Step 4. Analyze KPIs
# -------------------

avg_latency = df['latency_ms'].mean()
avg_uptime = df['uptime_percent'].mean()
avg_packet_loss = df['packet_loss_rate'].mean()
total_bandwidth = df['bandwidth_usage_mb'].sum()

print("\n Network Performance Summary:")
print(f"Average Latency: {avg_latency:.2f} ms")
print(f"Average Uptime: {avg_uptime:.2f}%")
print(f"Average Packet Loss: {avg_packet_loss:.3f}%")
print(f"Total Bandwidth Usage: {total_bandwidth:.2f} MB")

print("\nTelecom Data Pipeline completed successfully!")

    
