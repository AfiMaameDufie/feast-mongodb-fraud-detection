"""
Retrieves point-in-time training data from Feast's offline store, then
"trains" a z-score model on it.

The model parameters are written to training/model_params.json so that the
Django view reads them instead of having to copy them in by hand.
"""

import json
from pathlib import Path

import pandas as pd
from feast import FeatureStore

BASE_DIR = Path(__file__).resolve().parent.parent
TRANSACTIONS_PARQUET_FILE = BASE_DIR / "data" / "transactions.parquet"
PARAMS_PATH = Path(__file__).resolve().parent / "model_params.json"

store = FeatureStore(repo_path=str(BASE_DIR / "feature_repo" / "feature_repo"))
transactions_df = pd.read_parquet(TRANSACTIONS_PARQUET_FILE)

entity_df = transactions_df[["user_id", "event_timestamp"]].copy()

training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "transaction_features:amount",
        "transaction_features:category",
        "transaction_features:location",
    ],
).to_df()

print(training_df.head(10))
print(f"\nPulled {len(training_df)} rows of training data.")

# --- The "model": mean and standard deviation of amount ---
# A transaction is flagged if it falls more than 2 standard deviations
# from the mean. This is the entire model -- two numbers and a formula.
TRAIN_MEAN_AMOUNT = float(training_df["amount"].mean())
TRAIN_STD_AMOUNT = float(training_df["amount"].std())

PARAMS_PATH.write_text(
    json.dumps(
        {
            "mean_amount": TRAIN_MEAN_AMOUNT,
            "std_amount": TRAIN_STD_AMOUNT,
            "z_score_threshold": 2.0,
        },
        indent=2,
    )
    + "\n"
)

print("\nTrained model parameters:")
print(f"TRAIN_MEAN_AMOUNT = {TRAIN_MEAN_AMOUNT}")
print(f"TRAIN_STD_AMOUNT = {TRAIN_STD_AMOUNT}")
print(f"\nWrote parameters to {PARAMS_PATH}")
