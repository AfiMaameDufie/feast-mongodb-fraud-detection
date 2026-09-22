"""
Confirms Feast can read materialized features back out of MongoDB
via get_online_features() -- the same call the Django scoring view
will make at request time.

The work is behind a __main__ guard because `feast apply` imports every
module in the feature repo to discover definitions. Without the guard the
lookup would run during `feast apply`, before the feature view is registered.
"""

from pathlib import Path

from feast import FeatureStore


def main():
    store = FeatureStore(repo_path=str(Path(__file__).resolve().parent))

    entity_rows = [{"user_id": 2}]

    online_features = store.get_online_features(
        features=[
            "transaction_features:amount",
            "transaction_features:category",
            "transaction_features:location",
        ],
        entity_rows=entity_rows,
    ).to_dict()

    print(online_features)


if __name__ == "__main__":
    main()
