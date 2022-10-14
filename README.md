# About
<!-- UPDATE VERSION IN BADGE MANUALLY -->
![PyPI Version](https://img.shields.io/badge/pypi-v0.2.0-orange)
![Build](https://img.shields.io/github/workflow/status/andrewt110216/iq-tester-game/Tests?style=plastic)

`iqtester` is a simple command-line version of the classic game "IQ Tester"

[PyPI Home Page](https://pypi.org/project/iqtester/)

# Quick Start

## How to Play

IQ Tester is played on a triangular board, typically with 5 rows of holes and pegs.

Start with any one hole empty. As you jump the pegs remove them from the board.

Try to leave only one peg. See how you rate!

## Support Python Versions

Python 3.7+

## Mac / Linux
```
pip install iqtester
```

## Windows
```
py -m pip install iqtester
```

## Start Playing
```
python3 -m iqtester
```

# Demos

## Gameplay

*A simple (albeit not very successful!) game looks like this.*

*As the game begins, focus on the bottom of the screen to see the current board.*

<img src="demo-gifs/play.gif">

<br>

## Feature: Undo a Jump (Go Back)

*If you make a mistake, or see a better move, use '.' to undo your last move!*

<img src="demo-gifs/back.gif">

<br>

## Multiple Pegs to Jump

*If you pick a peg that has multiple potential jumps, the pegs to jump will be highlighted.*

*Choose the peg you'd like to jump over!*

<img src="demo-gifs/multiple-jumps.gif">

<br>

## Change Board Size

*The size of the board can be changed to have 4, 5, or 6 rows.*

<img src="demo-gifs/increase-size.gif">

<br>

## Ask for a Hint

*Request a hint using '>' to see the move that leads to the best possible outcome.*

*This feature is only available with 13 or fewer pegs.*

<img src="demo-gifs/hint.gif">

<br>