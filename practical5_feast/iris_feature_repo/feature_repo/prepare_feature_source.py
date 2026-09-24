import pandas as pd
from pathlib import Path

# Experiment 4 input
input_file = Path(
    "C:/Users/kalpe/mlops-iris-classifier/data/processed/iris_features.csv"
)

# Feast output
output_file = Path("data/iris_features.parquet")

# Read Experiment 4 features
df = pd.read_csv(input_file)

# Create entity ID
df.insert(0, "sample_id", range(len(df)))

# Create event timestamps
start_time = pd.Timestamp(
    "2026-08-15 15:20:02",
    tz="UTC"
)

df["event_timestamp"] = pd.date_range(
    start=start_time,
    periods=len(df),
    freq="min"
)

# Created timestamp
df["created_timestamp"] = df["event_timestamp"]

# Make sure output directory exists
output_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Save as Parquet
df.to_parquet(
    output_file,
    index=False
)

print(f"Wrote {len(df)} rows to {output_file}")
