import random
import statistics
import time

from src.utils.io_utils import (
    add_line_to_file,
    read_file_lines,
)
from src.utils.parallel import PRIORITY_1, PRIORITY_2, MultiRunner
from src.utils.utils import gen_fake_msr, measure_time

msr_log_file = ".\\msr.log"
cfg_file = ".\\user_cfg.txt"

@measure_time
def gather_metrics(log_file=msr_log_file, io_issue=False):
    """Get some [fake] metrics and save to a log file."""
    batched_res = []
    for _ in range(1000):
        msr = gen_fake_msr()
        if io_issue is True:
            add_line_to_file(msr_log_file, msr, flush=True)
        else:
            batched_res.append(msr)
    if io_issue is False:
        add_line_to_file(msr_log_file, "\n".join([msr for msr in batched_res]))
    return io_issue

@measure_time
def read_conf(file_path=cfg_file):
    """Read conf file from disk."""
    return read_file_lines(file_path)

@measure_time
def noop(period: float):
    """Sleep for a period of seconds."""
    time.sleep(period)


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

def io_cont(p1_count=1, p2_count=1, io_issue=False):
    runner = MultiRunner()
    for func in [gather_metrics, read_conf, noop]:
        runner.add_function(func.__name__, func)

    for _ in range(p2_count):
        runner.add_task('gather_metrics', PRIORITY_2, (msr_log_file, io_issue))

    for _ in range(p1_count):
        runner.add_task('read_conf', PRIORITY_1, (cfg_file,))
        # add auxiliary noop task to simulate interval between two requests for readiing cfg
        runner.add_task('noop', PRIORITY_1, (random.uniform(0.1, 2),))
    runner.run()
    durations = {}
    for r in runner.results:
        func = r['f_name']
        duration = r['duration']
        durations.setdefault(func, []).append(duration)

    return durations


if __name__ == '__main__':
    io_cont(p1_count=100, p2_count=1000, io_issue=False)
    io_cont(p1_count=100, p2_count=1000, io_issue=True)
