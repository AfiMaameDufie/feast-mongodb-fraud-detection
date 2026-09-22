from django.conf import settings
from feast import FeatureStore

FEATURE_REPO_PATH = settings.BASE_DIR / "feature_repo" / "feature_repo"
_store = FeatureStore(repo_path=str(FEATURE_REPO_PATH))


def get_latest_transaction_features(user_id: int) -> dict:
    """
    Looks up the most recent materialized transaction features for a
    user_id from MongoDB (the online store) via Feast.
    """
    result = _store.get_online_features(
        features=[
            "transaction_features:amount",
            "transaction_features:category",
            "transaction_features:location",
        ],
        entity_rows=[{"user_id": user_id}],
    ).to_dict()

    return {key: values[0] for key, values in result.items()}