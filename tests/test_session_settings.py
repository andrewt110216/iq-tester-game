import io
from iqtester.session import Session


# TODO Write tests for the following functions:
# update pause
# settings menu

def test_session_update_board_size(monkeypatch, capsys):

    # Initialize new session with default board size
    s = Session()
    assert s.board_size == 5

    # Set standard input as user inputs to update board size
    # First attempt invalid inputs, expecting to be reprompted
    user_input = io.StringIO(
        "a\n"   # Invalid input: string
        "\r\n"  # Invalid input: carriage return
        "3\n"   # Invalid input: minimum board size is 4
        "7\n"   # Invalid input: maximum board size is 7
        "6\n"   # Valid input
    )
    monkeypatch.setattr('sys.stdin', user_input)

    # Call update board size with standard input set
    s.update_board_size()

    # Check board size was updated
    assert s.board_size == 6

    # Check print statements
    out, _ = capsys.readouterr()

    # Iterate over each line in output categorizing each line
    prompt_str = "Enter desired board size (4 to 6)"
    must_be_int_str = "Board size must be an integer. Try again."
    outside_range_str = "Board size must be 4-6 not"
    size_updated_str = "Updating board size to 6..."
    prompt = must_be_int = outside_range = size_updated = blanks = 0
    for line in out.split("\n"):
        prompt += prompt_str in line
        must_be_int += must_be_int_str in line
        outside_range += outside_range_str in line
        size_updated += size_updated_str in line
        blanks += line == ''

    # Compare counts to expectations
    assert prompt == 5  # Original plus reprompt for each invalid input
    assert must_be_int == 2  # String and carriage return invalid inputs
    assert outside_range == 2  # 3 and 7 outside of range
    assert size_updated == 1  # Printed after valid input (6)

    # Expect a blank row between each non-blank row, plus an extra at end
    # First line (1) plus blank after each non-blank (10), plus final blank (1)
    assert blanks == 12
