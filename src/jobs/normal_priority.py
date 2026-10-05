"""
Functions to be used as MultiRunner.runner_functions to process NORMAL PRIORITY and medium heavy tasks.
Expected tasks volume: high.

"""
from src.fault_flags import IO_CONTENTION
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
