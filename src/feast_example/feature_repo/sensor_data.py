from pathlib import Path

from feast import (Entity, FeatureService, FeatureView, FileSource,
                   PushSource)
from feast.value_type import ValueType

from feast_example.stream_job import ds

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
)

sensor_stats_push_source = PushSource(
    name="push_sensor_statistics",
    batch_source=sensor_stats_source,
)

# Define a FeatureView
sensor_stats_view = FeatureView(
    name="sensor_statistics",
    entities=[sensor],
    schema=ds.get_feast_schema(),
    source=sensor_stats_push_source,
    online=True,
)

# Define a FeatureService
sensor_feature_service = FeatureService(
    name="sensor_service",
    features=[sensor_stats_view],
    description="Feature service for retrieving sensor statistics",
)
