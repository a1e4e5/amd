import time

from src.jobs.normal_priority import get_back_in_next_minute, some_calculations
from src.runner import PRIORITY_1, PRIORITY_2, MultiRunner
from src.utils.utils import gen_stats, measure_time


@measure_time
def noop(period: float):
    """Sleep for a period of seconds."""
    time.sleep(period)


def test_cpu_cont():
    """CPU contention"""
    runner = MultiRunner(max_p1_workers=1, max_p2_workers=10)
    for func in [get_back_in_next_minute, some_calculations, noop]:
        runner.add_function(func.__name__, func)
    for _ in range(20):
        runner.add_task('get_back_in_next_minute', PRIORITY_2, ())

    iterations = 1000
    for _ in range(20):
        runner.add_task('some_calculations', PRIORITY_1, (iterations,))

    runner.run()
    durations = {}
    for r in runner.results:
        func = r['f_name']
        duration = r['duration']
        durations.setdefault(func, []).append(duration)
    p1_durations = durations['some_calculations']
    p1_stats = gen_stats(p1_durations)
    assert p1_stats["max-min/avg"] < 0.3, "CPU bounded operations should be pretty stable if no CPU contention"
