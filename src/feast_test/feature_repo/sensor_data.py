from datetime import timedelta
from pathlib import Path

from feast import Entity, FeatureView, Field, FileSource, PushSource
from feast.types import Float64, Int64, String, UnixTimestamp
from feast.value_type import ValueType

# Define an entity for the sensor
sensor = Entity(
    name="sensor",
    value_type=ValueType.STRING, 
    join_keys=["sensor_name"],
    description="A unique identifier for each sensor",
)

# Define the data source for our features
sensor_stats_source = FileSource(
    path=str(Path(__file__).parent / "./data/sensor_stats.parquet"),
    timestamp_field="window_start_time",
    created_timestamp_column="created",
)

sensor_stats_push_source = PushSource(
    name="push_sensor_statistics",
    batch_source=sensor_stats_source,
)

# Define a FeatureView
sensor_stats_view = FeatureView(
    name="sensor_statistics",
    entities=[sensor],
    schema=[
        Field(name="sensor_name", dtype=String),
        Field(name="count", dtype=Int64),
        Field(name="min", dtype=Float64),
        Field(name="max", dtype=Float64),
        Field(name="average", dtype=Float64),
        Field(name="window_start_time", dtype=UnixTimestamp),
        Field(name="window_end_time", dtype=UnixTimestamp),
    ],
    source=sensor_stats_push_source,
    online=True,
)
