import random
import statistics
import string
import time
from functools import wraps


def measure_time(func):
    """Call function func, measure time of execution and return a tuple (duration, func_result) """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        return duration, result

    return wrapper


def gen_fake_msr() -> str:
    """Generate fake measurement vector [metric_name, timestamp, value_float, value_int].
    Both metric_name and values should be random.
    Return in a csv string format.
    """
    score_min = 0
    score_max = 100
    name = f"metric__{"".join(random.choices(string.ascii_lowercase, k=random.randint(5,10)))}"
    msr_tuple = (name, time.time(), random.uniform(score_min, score_max), random.randint(score_min, score_max),)
    msr_str_format = ",".join([str(elem) for elem in msr_tuple])
    return msr_str_format


def gen_stats(durations: list[float]) -> dict:
    """Calculate and return some stats for a list of a durations."""
    percentiles = statistics.quantiles(durations, n=100)
    mean = statistics.mean(durations)
    p99 = percentiles[98]
    median = percentiles[49]
    stats = {"min": min(durations),
             "max": max(durations),
             "avg": mean,
             "p99": p99,
             "median": median,
             "p99/median": p99/median,
             "p99/avg": p99/mean,
            }
    return stats