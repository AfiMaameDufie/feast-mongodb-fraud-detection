"""Generates random transactions data for the Feast + MongoDB tutorial."""

from pathlib import Path

import pandas as pd
import numpy as np

OUTPUT_PATH = Path(__file__).resolve().parent / "transactions.parquet"

random_generator = np.random.default_rng(seed=42)
N, FRAUD_RATE = 50, 0.02

df = pd.DataFrame({
    "user_id": random_generator.integers(1, 9, N),
    "transaction_id": [f"txn_{i:04d}" for i in range(N)],
    "amount": random_generator.lognormal(mean=3.5, sigma=0.6, size=N).round(2),
    "category": random_generator.choice(["food", "utilities", "entertainment", "travel", "shopping"], size=N),
    "location": random_generator.choice(["Accra", "Lagos", "New York", "London", "Paris"], size=N),
    # Timezone-aware: Django runs with USE_TZ = True, and Feast expects UTC.
    "event_timestamp": pd.Timestamp("2026-07-01", tz="UTC") + pd.to_timedelta(random_generator.integers(0, 30 * 24 * 60, N), unit="m"),
}).sort_values("event_timestamp").reset_index(drop=True)

# Add a small percentage of fraudulent transactions
fraud_indices = df.sample(frac=FRAUD_RATE, random_state=42).index
df["is_fraudulent"] = False
df.loc[fraud_indices, "is_fraudulent"] = True
df.loc[fraud_indices, "amount"] *= random_generator.uniform(5, 10, len(fraud_indices))   # Inflate the amount for fraudulent transactions
df["created_timestamp"] = df["event_timestamp"]

df.to_parquet(OUTPUT_PATH, index=False)
print(f"Wrote {len(df)} transactions to parquet file, {df['is_fraudulent'].sum()} of which are fraudulent.")

