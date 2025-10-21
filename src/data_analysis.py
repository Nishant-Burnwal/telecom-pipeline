import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

#Connect to the database
connection_string = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
engine = create_engine(connection_string)

# Load data from MySQL table
query = "SELECT * FROM network_logs;"
df = pd.read_sql(query, con=engine)

print("Data loaded from MySQL with shape:", df.shape)
print(df.head())

# ----------------
# 1. Overall KPIs
# ----------------

avg_latency = df['latency_ms'].mean()
avg_uptime = df['uptime_percent'].mean()
avg_packet_loss = df['packet_loss_rate'].mean()
total_bandwidth = df['bandwidth_usage_mb'].sum()

print("\nOverall etwork KPIs:")
print(f"Average Latency (ms): {avg_latency:.2f} ms")
print(f"Average Uptime (%): {avg_uptime:.2f}%")
print(f"Average Packet Loss Rate (%): {avg_packet_loss:.2f}%")
print(f"Total Bandwidth Usage (MB): {total_bandwidth:.2f} MB\n")

# ----------------
# 2. KPIs by Region
# ----------------

region_summary = (
    df.groupby('region')
    .agg({
        'latency_ms': 'mean',
        'uptime_percent': 'mean',
        'packet_loss_rate': 'mean',
        'bandwidth_usage_mb': 'sum'
    })
    .reset_index()
    )

print("Regional performance summary:")
print(region_summary, "\n")

# ----------------
# 3. Detecy Underperforming Devices
# ----------------

poor_regions = region_summary[
    (region_summary["uptime_percent"] < 90) | (region_summary["packet_loss_rate"] > 1)
]

if not poor_regions.empty:
    print("Regions with underperforming metrics:")
    print(poor_regions)
else:
    print("All regions are performing within acceptable thresholds.")