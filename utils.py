import random
import time
from typing import Tuple

class UnsupportedInputException(Exception):
    """Class for raising exceptions on unsupported input"""
    pass

def gen_random_score(score_type: str) -> int | float:
    """Generate a random score (single number) of a type defined by score_type from 0..100 range."""
    score_min = 0
    score_max = 100
    if score_type == 'float':
        score = random.uniform(score_min, score_max)
    elif score_type == 'int':
        score = random.randint(score_min, score_max)
    else:
        raise UnsupportedInputException(f"Unsupported score_type {score_type}")
    return score


def gen_fake_msr(metric_name: str, msr_type: str) -> Tuple[str, float, int|float]:
    """Generate fake measurement vector [metric_name, timestamp, value].
    :rtype: Tuple[str, float, int|float]
    """
    return metric_name, time.time(), gen_random_score(msr_type)


