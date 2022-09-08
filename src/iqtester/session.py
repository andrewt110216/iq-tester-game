import time
from .formatter import Formatter, space
from .game import Game


class Session:
    """API for a session of gameplay of IQ Tester"""

    def __init__(self):
        self.f = Formatter(78)
        self.total_score = 0
        self.board_size = 5
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
        self.f.center("Edit Settings [s]", ['BOLD', 'RED'], in_w=w, in_b='|')
        self.f.center("Quit [q]", ['BOLD', 'RED'], in_w=w, in_b='|')

        # bottom border of menu
        self.f.center("", in_w=w, in_b='|')
        self.f.center('', fill='-', in_w=w - 2)

    def settings_menu(self):
        """Allow user to change certain gameplay settings"""
        # menu width
        w = 40

        # menu header
        self.f.center('', fill='-', in_w=w - 2)
        self.f.center("", in_w=w, in_b='|')
        self.f.center("SETTINGS MENU", ['BOLD'], in_w=w, in_b='|')
        self.f.center("", in_w=w, in_b='|')

        # menu options
        n = self.board_size
        self.f.center(f"Update Board Size [u]: {n}", in_w=w, in_b='|')
        self.f.center("Return to Main Menu [m]", in_w=w, in_b='|')

        # bottom border of menu
        self.f.center("", in_w=w, in_b='|')
        self.f.center('', fill='-', in_w=w - 2)

    @space
    def update_board_size(self):
        low = 4  # minimum board size (3 or less doesn't work)
        high = 6  # maximum board size (7 or more uses > 26 pegs)
        while True:
            n = self.f.prompt(f"Enter desired board size ({low} to {high}):")
            try:
                n = int(n)
                if low <= n <= high:
                    break
            except NameError:
                self.f.center("Board size must be an integer. Try again.")

        print()
        self.f.center(f"Updating board size to {n}...")
        self.board_size = n

    @space
    def footer(self):
        self.f.center("For even more fun compete with someone. Lots of luck!")
        self.f.center("Copyright (C) 1975 Venture MFG. Co., INC. U.S.A.")
        self.f.center("Python package `iqtester` by Andrew Tracey, 2022.")
        self.f.center("Follow me: https://www.github.com/andrewt110216")

    @space
    def main_selection(self):
        """Let user select a menu option"""
        play = self.f.prompt("PRESS ENTER FOR NEW GAME")
        return play

    @space
    def setting_selection(self):
        """Let user select an option from the settings menu"""
        setting = self.f.prompt("Make a selection from the above options")
        return setting

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
            choice = self.main_selection().lower()
            if choice == "":
                self.game = Game(self.f, self.board_size)
                game_score = self.game.play()
                self.total_score += game_score
                self.played += 1
            elif choice == "s":
                self.settings_menu()
                setting_choice = self.setting_selection().lower()
                if setting_choice == "u":
                    self.update_board_size()
                    time.sleep(0.8)
                self.f.center("Returning to Main Menu...")
                time.sleep(1)
            else:
                self.quit()
