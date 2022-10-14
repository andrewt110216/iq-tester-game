# Changelog

## v0.2.0 (10/14/2022)

### Feature

- Added option to ask for a **hint** to solve for the optimal result and provide the next move
- Added settings option to change the pause time after completing a game

### Fix

- Improved efficiency of algorithms in Board and Game classes
- Improved comments in source code for readability

## v0.1.1 (09/14/2022)

### Feature

- Menus reformatted with left/right alignment for easier viewing

### Fix

- Roll back Python requirement from >=3.10 to >=3.7
  - v0.0.1 was mistakenly released with a requirement of Python >=3.7. It actually required >=3.10 due to the use of the `match-case` syntax.
  - Due to this mistake, users of 3.7-3.9 were able to download the package, which would fail to run on their versions.
  - This release removes the use of `match-case` and lowers the Python version requirement to >=3.7.

## v0.1.0 (09/07/2022)

### Feature

- Added option for user to change number of rows on the board to 4, 5, or 6

### Fix

- Improved gameplay, formatting, and spacing

### Tests

- Added automated linting to source code

## v0.0.3 (08/25/2022)

### Feature

- Added option for user to "go back" after making a jump

## v0.0.2 (08/25/2022)

### Fix

- Minor updates to gameplay and formatting

## v0.0.1 (08/24/2022)

- First release of `iqtester`