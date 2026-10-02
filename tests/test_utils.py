import pytest

from src.utils.score_gen import (
    UnsupportedInputException,
    gen_fake_msr,
    gen_random_score,
    score_max,
    score_min,
)


def test_gen_random_score__1():
    score1 = gen_random_score('float')
    score2 = gen_random_score('int')
    assert isinstance(score1, float)
    assert isinstance(score2, int)

@pytest.mark.repeat(1000)
# repeat due to non-deterministic nature of tested function
def test_gen_random_score__2():
    score1 = gen_random_score('float')
    score2 = gen_random_score('int')
    assert score_min <= score1 <= score_max
    assert score_min <= score2 <= score_max

def test_gen_random_score__bad_input():
    with pytest.raises(UnsupportedInputException):
        gen_random_score('fraction')

def test_gen_fake_msr():
    metric_name, timestamp_1, score = gen_fake_msr('fps', 'float')
    assert metric_name == 'fps'
    assert isinstance(timestamp_1, float)
    assert isinstance(score, float)
    _, timestamp_2, _ = gen_fake_msr('fps', 'float')
    assert timestamp_2 > timestamp_1, "Timestamp for newer result should be higher"


