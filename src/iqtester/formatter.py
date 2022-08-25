from functools import wraps


def space(f):
    @wraps(f)
    def wrapped(self, *args, **kwargs):
        print()
        return f(self, *args, **kwargs)

    return wrapped


class Formatter:
    """An API to control formatting of the command line interface"""

    def __init__(self, width):
        self.w = width

    # style formatting options {'name': ('string code', length of string code)}
    formats = {
        "PURPLE": ("\033[95m", 5),
        "CYAN": ("\033[96m", 5),
        "DARKCYAN": ("\033[36m", 5),
        "BLUE": ("\033[94m", 5),
        "GREEN": ("\033[92m", 5),
        "YELLOW": ("\033[93m", 5),
        "RED": ("\033[91m", 5),
        "BOLD": ("\033[1m", 4),
        "UNDERLINE": ("\033[4m", 4),
        "END": ("\033[0m", 4),
    }

    def center(self, msg, styles=[], fill=' ', in_w=0, in_b=''):
        """Style text and center across width and optional inner container"""

        # apply styles to message and inner container border
        fmt_start = ''
        fmt_chars = 0
        for style in styles:
            if style not in self.formats:
                raise NotImplementedError(f'Style "{style}" not implemented.')
            fmt_start += self.formats[style][0]
            fmt_chars += self.formats[style][1]
        msg = fmt_start + msg + self.formats['END'][0]
        fmt_chars += self.formats['END'][1]

        # margin refers to combined space on each side of inner container
        # note that border size is removed from inner width, not margin
        margin = self.w - in_w if in_w else 0
        lmargin = margin // 2

        # print left margin
        print(' ' * lmargin, end='')

        # calculate width for '.center' method inside of 'print' function
        #  + self.w (starting total width)
        #  - subtract margin
        #  - subtract size of inner container border
        #  + add number of formatting characters in msg that don't print
        # Each formatting code adds a certain number of characters to msg that
        # the print function considers when centering the output. If we do not
        # adjust for this, then the actual width of printed characters will
        # be less than the desired width (by exactly the number of fmt_chars)
        width = self.w - margin - 2 * len(in_b) + fmt_chars
        print(in_b + msg.center(width, fill) + in_b)

    def bold(self, text):
        return self.formats["BOLD"][0] + text + self.formats["END"][0], 8

    def red(self, text):
        return self.formats["RED"][0] + text + self.formats["END"][0], 8

    def apply(self, text, options=["BOLD"]):
        offset = 4  # END
        for format in options:
            code = self.formats[format][0]
            text = code + text
            offset += len(code)
        return text + self.formats["END"][0], offset + 1

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
