from datetime import timedelta
from feast import Entity, FeatureView, Field, FileSource
from feast.types import Float32, Int64, String
from feast.value_type import ValueType

# Entities are what we used to look up features and in this case is the customer_id
user = Entity(
    name="user_id", 
    join_keys=["user_id"], 
    value_type=ValueType.INT64,
)

# Directs Feast to the source of data(parquet file) as Feast does not go through the Django ORM to get the data.
transaction_source = FileSource(
    path="../../data/transactions.parquet",
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
