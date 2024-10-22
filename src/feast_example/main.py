import signal
import sys
from pathlib import Path

from feast import FeatureStore

from feast_example.stream_job import ds

if __name__ == "__main__":

    def signal_handler(_sig, _frame):
        print("You pressed Ctrl+C!")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    repo_path = Path(__file__).parent / "./feature_repo/"

    feature_service = FeatureStore(repo_path=str(repo_path.resolve()))
    ds.write_feast_feature(feature_service, "push_sensor_statistics")
