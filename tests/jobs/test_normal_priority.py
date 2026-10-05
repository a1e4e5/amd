
import time
from pathlib import Path

from src.jobs.normal_priority import get_and_save_metrics


def test_get_and_save_metrics(tmp_path, benchmark):
    """Test time of getting and saving metrics."""
    f_name = f"msr_{int(time.time())}.log"
    log_file_path = Path(tmp_path) / f_name
    benchmark(get_and_save_metrics, 500, log_file_path)

