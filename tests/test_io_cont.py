import random
import time
from pathlib import Path

from src.jobs.high_priority import get_file_lines_count, read_cfg
from src.jobs.normal_priority import get_and_save_metrics
from src.runner import PRIORITY_1, PRIORITY_2, MultiRunner
from src.utils.io_utils import (
    add_line_to_file,
)
from src.utils.utils import gen_stats, measure_time

log_file_name = "msr.log"
cfg_file_name = "user_cfg.txt"


@measure_time
def noop(period: float):
    """Sleep for a period of seconds."""
    time.sleep(period)



def test_io_cont(tmp_path):
    """IO"""
    cfg_file_path = Path(tmp_path) / cfg_file_name
    log_file_path = Path(tmp_path) / log_file_name
    add_line_to_file(str(cfg_file_path), "Dummy cfg content, just to create cfg file")
    runner = MultiRunner(max_p1_workers=1, max_p2_workers=10)
    for func in [get_and_save_metrics, read_cfg, noop, get_file_lines_count]:
        runner.add_function(func.__name__, func)
    for _ in range(5000):
        runner.add_task('get_and_save_metrics', PRIORITY_2, (300, log_file_path,))

    for _ in range(50):
        runner.add_task('read_cfg', PRIORITY_1, (cfg_file_path,))
        # add auxiliary noop task to simulate interval between two requests for reading cfg
        runner.add_task('noop', PRIORITY_1, (random.uniform(0.1, 0.5),))
        runner.add_task('get_file_lines_count', PRIORITY_1, (log_file_path,))

    runner.run()
    durations = {}
    for r in runner.results:
        func = r['f_name']
        duration = r['duration']
        durations.setdefault(func, []).append(duration)
    # save_metrics_stats = gen_stats(durations['get_and_save_metrics'])
    read_cfg_stats = gen_stats(durations['read_cfg'])
    get_file_lines_count_stats = gen_stats(durations['get_file_lines_count'])
    assert read_cfg_stats["p99/avg"] < 20, "Some tasks took much longer to complete than average"
    assert get_file_lines_count_stats["p99/avg"] < 20, "Some tasks took much longer to complete than average"

