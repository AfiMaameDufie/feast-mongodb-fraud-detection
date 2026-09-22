"""
 Retrieves point in time training data from Feast's offline store. 
 Then trains a z-score model using the data.
"""

import pandas as pd
from feast import FeatureStore

store = FeatureStore(repo_path="../feature_repo/feature_repo")
transactions_df = pd.read_parquet("../data/transactions.parquet")


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
TRAIN_MEAN_AMOUNT = training_df["amount"].mean()
TRAIN_STD_AMOUNT = training_df["amount"].std()

print(f"\nTrained model parameters:")
print(f"TRAIN_MEAN_AMOUNT = {TRAIN_MEAN_AMOUNT}")
print(f"TRAIN_STD_AMOUNT = {TRAIN_STD_AMOUNT}")