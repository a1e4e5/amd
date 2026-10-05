"""
Functions to be used as MultiRunner.runner_functions to process HIGH PRIORITY SHORT tasks.
Expected tasks volume: low / medium, short tasks.

"""

from src.utils.io_utils import (
    add_line_to_file,
    count_file_lines,
    read_file_lines,
)
from src.utils.utils import measure_time


@measure_time
def read_cfg(cfg_file_path: str) -> list[str]:
    """Read config file from disk using readlines"""
    return read_file_lines(cfg_file_path)


@measure_time
def add_line_to_cfg_file(cfg_file_path: str, new_line):
    """Append a new line to a config file. Create file if does not exist."""
    add_line_to_file(cfg_file_path, new_line)


@measure_time
def get_file_lines_count(cfg_file_path: str) -> list[str]:
    """Read number of lines in a file"""
    return count_file_lines(cfg_file_path)