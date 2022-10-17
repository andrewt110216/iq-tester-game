import pytest
from iqtester.session import Session
from iqtester.formatter import Formatter


def test_session_init():

    s = Session()

    # Check attributes
    assert isinstance(s.f, Formatter)
    assert s.played == 0
    assert s.total_score == 0
    assert s.board_size == 5
    assert s.keep_playing
