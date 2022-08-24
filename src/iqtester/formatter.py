from functools import wraps


def space(f):
    @wraps(f)
    def wrapped(self, *args, **kwargs):
        print()
        f(self, *args, **kwargs)
        print()

    return wrapped


class Formatter:
    """An API to control formatting of the command line interface"""

    def __init__(self, width):
        self.w = width

    formats = {
        "PURPLE": "\033[95m",
        "CYAN": "\033[96m",
        "DARKCYAN": "\033[36m",
        "BLUE": "\033[94m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "RED": "\033[91m",
        "BOLD": "\033[1m",
        "UNDERLINE": "\033[4m",
        "END": "\033[0m",
    }

    def bold(self, text):
        return self.formats["BOLD"] + text + self.formats["END"], 8

    def red(self, text):
        return self.formats["RED"] + text + self.formats["END"], 8

    def apply(self, text, options=["BOLD"]):
        offset = 4  # END
        for format in options:
            code = self.formats[format]
            text = code + text
            offset += len(code)
        return text + self.formats["END"], offset + 1

    def printf(self, text, offset=0):
        print(text.center(self.w + offset))

    def print_bar(self, text, offset=0):
        print(("|" + text + "|").center(self.w + offset))

    def print_row(self, text, inner_w, row, formatting=False):
        margin = (self.w - inner_w) // 2
        print(" " * margin + "|", end="")
        if formatting:
            pass
            padding = (inner_w - (row + 1) * 2) // 2
            print(" " * padding, end="")
            print(text, end="")
            print(" " * padding, end="")
        else:
            print(text.center(inner_w), end="")
        print("|" + " " * margin)

    def prompt(self, msg):
        msg = ">> " + msg + " >>"
        n = len(msg)
        msg, off = self.red(msg)
        print(msg.rjust((self.w // 2) + (n // 2) + off), end="")
        return input(" ")
