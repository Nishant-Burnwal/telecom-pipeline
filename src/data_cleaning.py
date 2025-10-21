# src/data_cleaning.py
import pandas as pd
import numpy as np

# Step 1: Read the raw CSV
df = pd.read_csv("data/telecom_network_logs_raw.csv")

print("Raw data loaded successfully!")
print("Initial shape:", df.shape)

# Step 2: Handle missing values
# Fill missing region/device_id with "Unknown"
df['region'] = df['region'].fillna('Unknown')
df['device_id'] = df['device_id'].fillna('Unknown')

# Fill missing latency with mean latency
if df['latency_ms'].isnull().any():
    df['latency_ms'] = df['latency_ms'].fillna(df['latency_ms'].mean())

# Step 3: Fix invalid packet loss or uptime values
df['packet_loss_rate'] = df['packet_loss_rate'].apply(lambda x: np.nan if x < 0 else x)
df['uptime_percent'] = df['uptime_percent'].apply(lambda x: np.nan if x < 0 or x > 100 else x)

# Step 4: Replace remaining NaNs with safe defaults
df = df.fillna({
    'packet_loss_rate': 0.0,
    'uptime_percent': 0.0,
    'latency_ms': 0.0
})

# Step 5: Show summary
print("\Cleaned data sample:")
print(df.head())

# Step 6: Save cleaned version
df.to_csv("telecom_network_logs_clean.csv", index=False)
print("\Cleaned data saved to telecom_network_logs_clean.csv")
