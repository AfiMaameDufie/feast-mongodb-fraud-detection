"""
Confirms Feast can read materialized features back out of MongoDB
via get_online_features() -- the same call the Django scoring view
will make at request time.
"""

from feast import FeatureStore

store = FeatureStore(repo_path=".")

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