from .formatter import Formatter, space
from .game import Game


class Session:
    """API for a session of gameplay of IQ Tester"""

    def __init__(self):
        self.f = Formatter(78)
        self.total_score = 0
        self.game = None
        self.played = 0
        self.keep_playing = True

    def average(self):
        if self.played == 0:
            return round(0, 1)
        return round(self.total_score / self.played, 1)

    @space
    def header(self):
        self.f.center('', fill='*', s=["BOLD", "BLUE"])
        self.f.center(' WELCOME TO IQ TESTER ', fill='*', s=["BOLD"])
        self.f.center('', fill='*', s=["BOLD", "BLUE"])

    @space
    def instructions(self):
        self.f.center("Start with any one hole empty.")
        self.f.center("As you jump the pegs remove them from the board.")
        self.f.center("Try to leave only one peg. See how you rate!.")

    @space
    def menu_options(self):
        """Display the main menu including statistics and gameplay options"""
        # menu width
        w = 40

        # menu header
        self.f.center('', fill='-', in_w=w - 2)
        self.f.center("", in_w=w, in_b='|')
        self.f.center("HOME MENU", ['BOLD'], in_w=w, in_b='|')
        self.f.center("", in_w=w, in_b='|')

        # game statistics
        msg = f"GAMES PLAYED: {self.played}"
        self.f.center(msg, ['BOLD', 'GREEN'], in_w=w, in_b='|')
        msg = f"YOUR TOTAL SCORE: {self.total_score}"
        self.f.center(msg, ['BOLD', 'GREEN'], in_w=w, in_b='|')
        msg = f"AVERAGE SCORE: {self.average()}"
        self.f.center(msg, ['BOLD', 'GREEN'], in_w=w, in_b='|')
        self.f.center("", in_w=w, in_b='|')

        # menu options
        self.f.center("New Game [ENTER]", ['BOLD', 'RED'], in_w=w, in_b='|')
        self.f.center("Quit [any letter]", ['BOLD', 'RED'], in_w=w, in_b='|')
        self.f.center("", in_w=w, in_b='|')
        self.f.center('', fill='-', in_w=w - 2)

    @space
    def footer(self):
        self.f.center("For even more fun compete with someone. Lots of luck!")
        self.f.center("Copyright (C) 1975 Venture MFG. Co., INC. U.S.A.")
        self.f.center("Python package `iqtester` by Andrew Tracey, 2022.")
        self.f.center("Follow me: https://www.github.com/andrewt110216")

    @space
    def select_option(self):
        """Let user select a menu option"""
        play = self.f.prompt("PRESS ENTER FOR NEW GAME")
        return play

    def quit(self):
        """Handle user selection to quit playing"""
        self.f.center("Thanks for playing!", s=['BOLD'])
        self.footer()
        self.keep_playing = False

    def start(self):
        """Drive gameplay"""
        self.header()
        self.instructions()
        while self.keep_playing:
            self.menu_options()
            choice = self.select_option()
            if choice == "":
                self.game = Game(self.f)
                game_score = self.game.play()
                self.total_score += game_score
                self.played += 1
            else:
                self.quit()
