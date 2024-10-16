import signal
import sys
from pathlib import Path

import pyarrow as pa
from feast import FeatureStore

from feast_test.stream_job import ds

if __name__ == "__main__":

    def signal_handler(_sig, _frame):
        print("You pressed Ctrl+C!")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        repo_path = Path(__file__).parent / "./feature_repo/"
        print(repo_path)
        # feature_service = FeatureStore(repo_path=str(repo_path.resolve()))

        # ds.write_feast_feature(feature_service, "push_sensor_statistics")
    except Exception as e:
        print(e)
