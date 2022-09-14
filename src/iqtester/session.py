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

    def get_average(self):
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
    def main_menu(self):
        """Display the main menu including statistics and gameplay options"""
        # menu width
        w = 40

        # menu header
        self.f.center('', fill='-', in_w=w - 2)
        self.f.center("", in_w=w, in_b='|')
        self.f.center("MAIN MENU", ['BOLD'], in_w=w, in_b='|')
        self.f.center("", in_w=w, in_b='|')

        # game statistics
        # format total and average scores for display
        sc = f"{self.total_score:,}"
        average = self.get_average()
        if average % 1 == 0:
            average = int(average)
        avg = f"{average:,}"

        # assemble strings for each statistic, aligned left and right
        l, r = 18, max(6, len(sc), len(avg)) + 1
        games_played = "GAMES PLAYED: ".ljust(l) + str(self.played).rjust(r)
        total_score = "YOUR TOTAL SCORE: ".ljust(l) + sc.rjust(r)
        average_score = "AVERAGE SCORE: ".ljust(l) + avg.rjust(r)

        # display each menu row with formatting
        formats = ['BOLD', 'GREEN']
        self.f.center(games_played, formats, in_w=w, in_b='|')
        self.f.center(total_score, formats, in_w=w, in_b='|')
        self.f.center(average_score, formats, in_w=w, in_b='|')
        self.f.center("", in_w=w, in_b='|')

        # gameplay options
        formats = ['BOLD', 'RED']
        new_game_row = "New Game".ljust(l, '.') + "[ENTER]".rjust(r, '.')
        settings_row = "Settings".ljust(l, '.') + "[s]".rjust(r, '.')
        quit_row = "Quit".ljust(l, '.') + "[q]".rjust(r, '.')
        self.f.center(new_game_row, formats, in_w=w, in_b='|')
        self.f.center(settings_row, formats, in_w=w, in_b='|')
        self.f.center(quit_row, formats, in_w=w, in_b='|')

        # bottom border of menu
        self.f.center("", in_w=w, in_b='|')
        self.f.center('', fill='-', in_w=w - 2)

    def settings_menu(self):
        """Allow user to change certain gameplay settings"""
        # menu width
        w = 40
        l, r = 18, 4

        # menu header
        self.f.center('', fill='-', in_w=w - 2)
        self.f.center("", in_w=w, in_b='|')
        self.f.center("SETTINGS MENU", ['BOLD'], in_w=w, in_b='|')
        self.f.center("", in_w=w, in_b='|')

        # menu options
        n = self.board_size
        size_row = f"Board Size ({n})".ljust(l, '.') + "[s]".rjust(r, '.')
        return_row = f"Return".ljust(l, '.') + "[r]".rjust(r, '.')
        self.f.center(size_row, in_w=w, in_b='|')
        self.f.center(return_row, in_w=w, in_b='|')

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
    def menu_selection(self):
        """Prompt user to select menu option and return lowercased choice"""
        return self.f.prompt("Select a menu option").lower()

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
            self.main_menu()
            main_choice = self.menu_selection()
            if main_choice == "":
                self.game = Game(self.f, self.board_size)
                game_score = self.game.play()
                self.total_score += game_score
                self.played += 1
            elif main_choice == "s":
                self.settings_menu()
                setting_choice = self.menu_selection()
                if setting_choice == "s":
                    self.update_board_size()
                    time.sleep(0.8)
                self.f.center("Returning to Main Menu...")
                time.sleep(1)
            else:
                self.quit()
