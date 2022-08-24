from .formatter import Formatter, space
from .game import Game


class Session:
    """API for a session of gameplay of IQ Tester"""

    def __init__(self):
        self.keep_playing = True
        self.f = Formatter(79)
        self.total_score = 0
        self.game = None
        self.played = 0
        self.games = []

    def average(self):
        if self.played == 0:
            return round(0, 1)
        return round(self.total_score / self.played, 1)

    @space
    def header(self):
        self.f.printf(*self.f.apply(("*" * self.f.w), ["BOLD", "BLUE"]))
        self.f.printf(
            *self.f.apply(
                ' WELCOME TO IQ TESTER '.center(self.f.w, "*"),
                ["BOLD", "BLUE"],
            )
        )
        self.f.printf(*self.f.apply(("*" * self.f.w), ["BOLD", "BLUE"]))

    @space
    def instructions(self):
        print("Start with any one hole empty.".center(self.f.w))
        print(
            "As you jump the pegs remove them from the board.".center(self.f.w)
        )
        print(
            "Try to leave only one peg. See how you rate!.".center(
                self.f.w
            )
        )

    @space
    def menu_options(self):
        w = 40
        print(("-" * w).center(self.f.w))
        self.f.print_bar(" ".center(w))
        self.f.print_bar(*self.f.bold("HOME MENU".center(w)))
        self.f.print_bar(" ".center(w))
        self.f.print_bar(
            *self.f.apply(
                f"GAMES PLAYED: {self.played}".center(w), ["BOLD", "GREEN"]
            )
        )
        self.f.print_bar(
            *self.f.apply(
                f"YOUR TOTAL SCORE: {self.total_score}".center(w),
                ["BOLD", "GREEN"],
            )
        )
        self.f.print_bar(
            *self.f.apply(
                f"AVERAGE SCORE: {self.average()}".center(w), ["BOLD", "GREEN"]
            )
        )
        self.f.print_bar(" ".center(w))
        self.f.print_bar(
            *self.f.apply(
                "> Start new game (ENTER)".center(w), ["BOLD", "RED"]
            )
        )
        self.f.print_bar(
            *self.f.apply("> QUIT (any letter)".center(w), ["BOLD", "RED"])
        )
        self.f.print_bar(" ".center(w))
        print(("-" * w).center(self.f.w))

    @space
    def footer(self):
        print(
            "For even more fun compete with someone. Lots of luck!".center(
                self.f.w
            )
        )
        print(
            "Copyright (C) 1975 Venture MFG. Co., INC. U.S.A.".center(self.f.w)
        )
        print(
            "Python package `iq-tester` by Andrew Tracey, 2022.".center(
                self.f.w
            )
        )
        print(
            "Follow me: https://www.github.com/andrewt110216".center(self.f.w)
        )

    def select_option(self):
        print()
        play = self.f.prompt("PRESS ENTER FOR NEW GAME")
        return play

    @space
    def quit(self):
        self.f.printf(*self.f.bold("Thanks for playing!"))
        self.footer()
        self.keep_playing = False

    def start(self):
        self.header()
        self.instructions()
        while self.keep_playing:
            self.main_menu()

    def main_menu(self):
        self.menu_options()
        choice = self.select_option()
        if choice.lower() == "":
            if self.game:
                self.games.append(self.game)
            self.game = Game(self.f)
            self.total_score += self.game.play()
            self.played += 1
        else:
            self.quit()
