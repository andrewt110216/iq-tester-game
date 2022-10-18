from iqtester.session import Session
from iqtester.formatter import Formatter


# TODO Write tests for the following functions:
# quit
# menu_selection
# footer
# print instructions
# print new session header
# main menu
# start

def test_session_init():

    s = Session()

    # Test attributes
    assert isinstance(s.f, Formatter)
    assert s.played == 0
    assert s.total_score == 0
    assert s.board_size == 5
    assert s.game is None


def test_session_get_average():

    s = Session()

    # Initial session average should be 0
    assert s.get_average() == 0.0

    # Update score and number of games played
    s.total_score = 10
    s.played = 1
    assert s.get_average() == 10.0

    s.total_score = 35
    s.played = 2
    assert s.get_average() == 17.5

    s.total_score = 85
    s.played = 3
    assert s.get_average() == 28.3

    s.played = 4
    assert s.get_average() == round(85/4, 1)
