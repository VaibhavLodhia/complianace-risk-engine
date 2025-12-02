"""
Data Generation Script for Compliance Risk Engine

This script generates synthetic data and saves it to CSV files.
Run this script first before running compliance_risk_engine.py
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

print("=" * 80)
print("Data Generation Script")
print("=" * 80)
print()

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# ============================================================================
# GENERATE METADATA
# ============================================================================
print("Generating metadata...")
n_assets = 500
df_metadata = pd.DataFrame({
    'Data_Asset_ID': [f'ASSET_{i:04d}' for i in range(1, n_assets + 1)],
    'PHI_Flag': np.random.choice([True, False], size=n_assets, p=[0.3, 0.7]),
    'Encryption_Status': np.random.choice(['Encrypted', 'Plain'], size=n_assets, p=[0.6, 0.4])
})

metadata_path = 'data/metadata.csv'
df_metadata.to_csv(metadata_path, index=False)
print(f"  [OK] Saved {len(df_metadata)} assets to {metadata_path}")
print(f"    - PHI assets: {df_metadata['PHI_Flag'].sum()}")
print(f"    - Plain text assets: {(df_metadata['Encryption_Status'] == 'Plain').sum()}")
print()

# ============================================================================
# GENERATE ACCESS LOGS
# ============================================================================
print("Generating access logs...")
n_logs = 100000
n_users = 100
start_date = datetime(2024, 1, 1)

# Generate timestamps (spread over 6 months)
timestamps = []
for _ in range(n_logs):
    days_offset = np.random.randint(0, 180)
    hours_offset = np.random.randint(0, 24)
    minutes_offset = np.random.randint(0, 60)
    timestamp = start_date + timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)
    timestamps.append(timestamp)

df_access_logs = pd.DataFrame({
    'Timestamp': timestamps,
    'User_ID': [f'USER_{i:03d}' for i in np.random.randint(1, n_users + 1, n_logs)],
    'Data_Asset_ID': np.random.choice(df_metadata['Data_Asset_ID'], n_logs),
    'Access_Type': np.random.choice(['Read', 'Write'], n_logs, p=[0.7, 0.3]),
    'IP_Location': np.random.choice(['US', 'EU', 'AS'], n_logs, p=[0.6, 0.25, 0.15])
})

print(f"  [OK] Generated {len(df_access_logs)} access log entries")
print()

# ============================================================================
# INJECT ANOMALIES
# ============================================================================
print("Injecting 2,500 high-risk anomalies...")
n_anomalies = 2500

# Merge to get metadata info
df_access_logs = df_access_logs.merge(
    df_metadata[['Data_Asset_ID', 'PHI_Flag', 'Encryption_Status']],
    on='Data_Asset_ID',
    how='left'
)

# Identify normal rows (will be used to replace with anomalies)
normal_indices = df_access_logs.index.tolist()
np.random.shuffle(normal_indices)
anomaly_indices = normal_indices[:n_anomalies]

# Create anomaly conditions
anomaly_rows = []
for idx in anomaly_indices:
    row = df_access_logs.loc[idx].copy()
    
    # Randomly select one of the three anomaly types
    anomaly_type = np.random.choice(['plain_phi', 'off_hours', 'non_us'], p=[0.4, 0.3, 0.3])
    
    if anomaly_type == 'plain_phi':
        # Access to Plain text PHI asset
        plain_phi_assets = df_metadata[
            (df_metadata['PHI_Flag'] == True) & 
            (df_metadata['Encryption_Status'] == 'Plain')
        ]['Data_Asset_ID'].values
        if len(plain_phi_assets) > 0:
            row['Data_Asset_ID'] = np.random.choice(plain_phi_assets)
            row['PHI_Flag'] = True
            row['Encryption_Status'] = 'Plain'
    
    elif anomaly_type == 'off_hours':
        # Outside business hours (9 PM - 5 AM, i.e., hour >= 21 or hour < 5)
        hour = np.random.choice(list(range(21, 24)) + list(range(0, 5)))
        new_timestamp = row['Timestamp'].replace(hour=hour, minute=np.random.randint(0, 60))
        row['Timestamp'] = new_timestamp
    
    elif anomaly_type == 'non_us':
        # Non-US IP address
        row['IP_Location'] = np.random.choice(['EU', 'AS'])
    
    anomaly_rows.append(row)

# Replace the selected rows with anomalies
df_access_logs.loc[anomaly_indices] = anomaly_rows

# ============================================================================
# CREATE POLICY VIOLATION LABELS
# ============================================================================
print("Creating Policy_Violation labels...")
df_access_logs['Policy_Violation'] = 0

# Label anomalies based on the three criteria
for idx, row in df_access_logs.iterrows():
    violation = False
    
    # Check: Plain text PHI access
    if row['PHI_Flag'] and row['Encryption_Status'] == 'Plain':
        violation = True
    
    # Check: Outside business hours (9 PM - 5 AM)
    hour = row['Timestamp'].hour
    if hour >= 21 or hour < 5:
        violation = True
    
    # Check: Non-US IP
    if row['IP_Location'] != 'US':
        violation = True
    
    df_access_logs.loc[idx, 'Policy_Violation'] = 1 if violation else 0

print(f"  [OK] Policy violations detected: {df_access_logs['Policy_Violation'].sum()} out of {len(df_access_logs)}")
print(f"    Violation rate: {df_access_logs['Policy_Violation'].mean():.2%}")
print()

# ============================================================================
# SAVE ACCESS LOGS
# ============================================================================
access_logs_path = 'data/access_logs.csv'
df_access_logs.to_csv(access_logs_path, index=False)
print(f"  [OK] Saved access logs to {access_logs_path}")
print(f"    File size: {os.path.getsize(access_logs_path):,} bytes")
print()

print("=" * 80)
print("Data Generation Complete!")
print("=" * 80)
print()
print("Generated files:")
print(f"  - {metadata_path}")
print(f"  - {access_logs_path}")
print()
print("You can now run: python compliance_risk_engine.py")

