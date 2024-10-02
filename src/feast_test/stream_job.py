"""stream_aggregate example."""

import json
import signal
import sys
from pathlib import Path

import pandas as pd
import pyarrow as pa
from denormalized import Context
from denormalized.datafusion import col
from denormalized.datafusion import functions as f
from denormalized.datafusion import lit
from feast import FeatureStore
from feast.data_source import PushMode


# pyright: reportUnknownMemberType=false
def signal_handler(_sig, _frame):
    print("You pressed Ctrl+C!")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

bootstrap_server = "localhost:9092"

sample_event = {
    "occurred_at_ms": 100,
    "sensor_name": "foo",
    "reading": 0.0,
}

try:
    repo_path = Path(__file__).parent / "./feature_repo/"
    fs = FeatureStore(repo_path=str(repo_path.resolve()))
except Exception as e:
    print("Exception!!")
    print(e)


def sink_to_feast(rb: pa.RecordBatch):
    df: pd.DataFrame = rb.to_pandas()

    # This is required for feast to write ingestion
    df["created"] = df["window_start_time"]

    try:
        fs.push("push_sensor_statistics", df, to=PushMode.ONLINE)
    except Exception as e:
        print(e)


ctx = Context()
ds = ctx.from_topic("temperature", json.dumps(sample_event), bootstrap_server)

# pyright: reportUnknownMemberType=false
ds.window(
    [col("sensor_name")],
    [
        f.count(col("reading"), distinct=False, filter=None).alias("count"),
        f.min(col("reading")).alias("min"),
        f.max(col("reading")).alias("max"),
        f.avg(col("reading")).alias("average"),
    ],
    1000,
    None,
).filter(col("max") > (lit(113))).sink_python(sink_to_feast)
