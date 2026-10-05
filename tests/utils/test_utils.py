import pytest
from src.utils.utils import (
    gen_fake_msr,
)


@pytest.mark.repeat(100)
def test_gen_gen_fake_msr():
    score1 = gen_fake_msr()
    score2 = gen_fake_msr
    assert isinstance(score1, str)
    assert isinstance(score2, str)
    assert score1.count(",") == 3, "Expected 4 elements splitted with commas"
    assert score2.count(",") == 3, "Expected 4 elements splitted with commas"
    assert score1 != score2, "Expected random measurements, got the same"

