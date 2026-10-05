from src.faults.io_cont import cfg_file_name, io_cont, log_file_name
from src.utils.utils import gen_stats


def test_io_cont(tmp_path):
    durations = io_cont(tmp_path, cfg_file_name, log_file_name, p1_count=10, p2_count=1000, io_issue=False)
    gen_stats(durations)

