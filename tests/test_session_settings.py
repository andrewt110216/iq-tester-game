from io import StringIO
from typing import Any, List
from iqtester.session import Session


def categorize_output(output: str, categories: List[str]) -> List[int]:
    """Count the number of lines matching each category"""
    counts = [0] * len(categories)
    for line in output.split('\n'):
        # For all categories except blank, check if category is `in`` line
        for i, category in enumerate(categories[:-1]):
            if category in line:
                counts[i] += 1
        # Check if line is blank
        if line == categories[-1]:
            counts[-1] += 1
    return counts


def assert_counts(key, counts: List[int], expected_counts: List[int]) -> None:
    """Assert that each count equals its expected value"""
    print(key)  # for debugging failed tests
    for i, count in enumerate(counts):
        assert count == expected_counts[i]


def helper(
    key: str,
    args: tuple,
    user_input: StringIO,
    expected_counts: List[int],
    new_val: Any,
    monkeypatch,
    capsys
):
    """
    Template function to test updating a setting

    Parameters
    ----------
    key : str
        Key of setting in settings_menu_map
    args : tuple
        Value of key in settings_menu_map
    user_input : StringIO
        A simulated file object where each line is passed as the user input
        at a prompt in a session of IQ Tester
    expected_counts : List[int]
        Expected count of adjacent category in standard output
    new_val : Any
        Value to which setting should be updated
    monkeypatch
        Pytest argument that allows us to set the standard input variable
    capsys
        Pytest argument that allows us to capture standard output
    """

    s = Session(msg_pause=0.0)  # Reduce testing time

    # Set standard input and call update_settings method
    monkeypatch.setattr('sys.stdin', user_input)
    s.update_setting(*args)

    # Check that setting was updated correctly
    assert getattr(s, args[0]) == new_val

    # List of strings to match each category of output
    categories = [
        f"Enter desired {args[1]}",             # prompt
        f"{args[1]} must be",                   # out of range
        f"{args[1]} must of {str(args[2])}",    # invalid type
        f"Updating {args[1]} to {new_val}...",  # successful update
        "",                                     # blank rows
    ]

    # Check output against expectations
    output, _ = capsys.readouterr()
    counts = categorize_output(output, categories)
    assert_counts(key, counts, expected_counts)


def test_session_update_settings_all(monkeypatch, capsys):
    """Test updating each customizable setting"""

    # Mapping of user inputs to standard input to test each setting
    # Expected Counts Indices: [prompt, range, type, update, blank]
    setting_test_args_map = {
        "b": {
            'user_inputs': StringIO(
                'a\n'       # invalid type
                '\r\n'      # invalid type
                '3\n'       # out of range
                '7\n'       # out of range
                '6\n'       # valid
            ),
            'expected_counts': [5, 2, 2, 1, 7],
            'new_val': 6,
        },
        "c": {
            'user_inputs': StringIO(
                'a\n'       # out of range
                '\r\n'      # out of range
                '1\n'       # out of range
                'PINK\n'    # out of range
                'RED\n'     # valid
            ),
            'expected_counts': [5, 4, 0, 1, 7],
            'new_val': 'RED',
        },
        "p": {
            'user_inputs': StringIO(
                'a\n'       # invalid type
                '\r\n'      # invalid type
                '-0.01\n'   # out of range
                '3.01\n'    # out of range
                '0.0\n'    # valid
            ),
            'expected_counts': [5, 2, 2, 1, 7],
            'new_val': 0.0,
        },
        "m": {
            'user_inputs': StringIO(
                'a\n'       # invalid type
                '\r\n'      # invalid type
                '-0.01\n'   # out of range
                '3.01\n'    # out of range
                '0.0\n'    # valid
            ),
            'expected_counts': [5, 2, 2, 1, 7],
            'new_val': 0.0,
        },
        "s": {
            'user_inputs': StringIO(
                'a\n'       # out of range
                '\r\n'      # out of range
                '1\n'       # out of range
                '!\n'       # out of range
                '*\n'       # valid
            ),
            'expected_counts': [5, 4, 0, 1, 7],
            'new_val': '*',
        },
        "t": {
            'user_inputs': StringIO(
                'a\n'       # out of range
                '\r\n'      # out of range
                '1\n'       # out of range
                '!\n'       # out of range
                '*\n'       # valid
            ),
            'expected_counts': [5, 4, 0, 1, 7],
            'new_val': '*',
        },
        "w": {
            'user_inputs': StringIO(
                'a\n'       # invalid type
                '\r\n'      # invalid type
                '28\n'      # out of range
                '92\n'      # out of range
                '50\n'      # valid
            ),
            'expected_counts': [5, 2, 2, 1, 7],
            'new_val': 50,
        },
    }

    # Get settings menu map from Session object
    s = Session()
    settings_menu_map_items = s.settings_menu_map.items()
    del s

    for key, args in settings_menu_map_items:
        inputs = setting_test_args_map[key]['user_inputs']
        expected = setting_test_args_map[key]['expected_counts']
        new_val = setting_test_args_map[key]['new_val']
        helper(key, args, inputs, expected, new_val, monkeypatch, capsys)
