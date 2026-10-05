"""
Functions to be used as MultiRunner.runner_functions to process NORMAL PRIORITY and medium heavy tasks.
Expected tasks volume: high.

"""
import time

from src.fault_flags import CPU_CONTENTION, IO_CONTENTION
from src.utils.io_utils import (
    add_line_to_file,
)
from src.utils.utils import gen_fake_msr, measure_time


@measure_time
def get_and_save_metrics(metrics_number, log_file_path):
    """
    Get fake metrics and save to a log file.
    :param metrics_number - number of metrics to be generated and saved
    :param log_file_path - full path for saving metrics
    :io_
    """
    batched_res = []
    for _ in range(metrics_number):
        msr = gen_fake_msr()
        if IO_CONTENTION:
            add_line_to_file(log_file_path, msr, flush=True)
        else:
            batched_res.append(msr)
    if not IO_CONTENTION:
        add_line_to_file(log_file_path, "\n".join([msr for msr in batched_res]))
    return metrics_number


@measure_time
def get_back_in_next_minute():
    """When entered, check time, and wait until time minute value increases - then return."""
    t = time.time()
    enter_minute = time.localtime(t).tm_min
    while True:
        t = time.time()
        current_minute = time.localtime(t).tm_min
        if current_minute > enter_minute:
            break
        if not CPU_CONTENTION:
            time.sleep(1)       # sleep does not use cpu, check condition in next second is enough


@measure_time
def some_calculations(iters):
    for n in range(iters):
        _ = 999999 ** 9999

@measure_time
def concat_str(list_of_str):
    t = time.time()
    while True:
        if CPU_CONTENTION:
            if time.time() - t > 15:
                break
        else:
            time.sleep(15)
            break
    return
    final_str = ""
    if CPU_CONTENTION:
        for elem in list_of_str:
            final_str += elem
    else:
        final_str = "".join(list_of_str)
    return final_str
