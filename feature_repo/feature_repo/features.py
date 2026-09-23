from datetime import timedelta
from pathlib import Path

from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, String
from feast.value_type import ValueType

# An entity is the key that features are looked up by.
user = Entity(name="user_id", join_keys=["user_id"], value_type=ValueType.INT64)

# Feast reads the Parquet file directly; it does not go through the Django ORM.
TRANSACTIONS_PARQUET_FILE = (
    Path(__file__).resolve().parents[2] / "data" / "transactions.parquet"
)

transaction_source = FileSource(
    path=str(TRANSACTIONS_PARQUET_FILE),
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

transaction_features = FeatureView(
    name="transaction_features",
    entities=[user],
    ttl=timedelta(days=365),
    schema=[
        Field(name="amount", dtype=Float32),
        Field(name="category", dtype=String),
        Field(name="location", dtype=String),
    ],
    source=transaction_source,
)
