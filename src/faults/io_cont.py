import random
import statistics
import time
from pathlib import Path

from src.utils.io_utils import (
    add_line_to_file,
    read_file_lines,
)
from src.utils.parallel import PRIORITY_1, PRIORITY_2, MultiRunner
from src.utils.utils import gen_fake_msr, measure_time

log_file_name = "msr.log"
cfg_file_name = "user_cfg.txt"
work_dir = "."


@measure_time
def gather_metrics(log_file_path, io_issue=False):
    """Get some [fake] metrics and save to a log file."""
    batched_res = []
    for _ in range(1000):
        msr = gen_fake_msr()
        if io_issue is True:
            add_line_to_file(log_file_path, msr, flush=True)
        else:
            batched_res.append(msr)
    if io_issue is False:
        add_line_to_file(log_file_path, "\n".join([msr for msr in batched_res]))
    return io_issue

@measure_time
def read_cfg(cfg_file_path):
    """Read config file from disk."""
    return read_file_lines(cfg_file_path)

@measure_time
def noop(period: float):
    """Sleep for a period of seconds."""
    time.sleep(period)

def create_cfg_file(cfg_file_path):
    """Create dummy cfg_file (to be available for I/O later)"""
    cfg_content = "# this is a dummy cfg file for i/o contention tests\ncfg_name=golden config"
    add_line_to_file(cfg_file_path, cfg_content)

def present(prefix, durations):
    percentiles = statistics.quantiles(durations, n=100)
    mean = statistics.mean(durations)
    p99 = percentiles[98]
    median = percentiles[49]
    nice = {f"{prefix} p99/avg": p99/mean,
            f"{prefix} median": median,
            f"{prefix} min": min(durations),
            f"{prefix} max": max(durations),
            f"{prefix} avg": statistics.mean(durations),
            f"{prefix} max-min": max(durations)-min(durations),
            }
    return nice

def io_cont(working_dir, cfg_file_name, log_file_name, p1_count=1, p2_count=1, io_issue=False):
    cfg_file_path = Path(working_dir) / cfg_file_name
    log_file_path = Path(working_dir) / log_file_name
    create_cfg_file(cfg_file_path)      # just to be available for I/O (reading)
    runner = MultiRunner()
    for func in [gather_metrics, read_cfg, noop]:
        runner.add_function(func.__name__, func)

    for _ in range(p2_count):
        runner.add_task('gather_metrics', PRIORITY_2, (log_file_path, io_issue))

    for _ in range(p1_count):
        runner.add_task('read_conf', PRIORITY_1, (cfg_file_path,))
        # add auxiliary noop task to simulate interval between two requests for readiing cfg
        runner.add_task('noop', PRIORITY_1, (random.uniform(0.1, 1),))
    runner.run()
    durations = {}
    for r in runner.results:
        func = r['f_name']
        duration = r['duration']
        durations.setdefault(func, []).append(duration)

    return durations


if __name__ == '__main__':
    io_cont(work_dir, cfg_file_name, log_file_name, p1_count=10, p2_count=1000, io_issue=False)
