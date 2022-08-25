from functools import wraps


def space(f):
    """Decorate class methods with a new line printed before execution"""

    @wraps(f)
    def wrapped(self, *args, **kwargs):
        print()
        res = f(self, *args, **kwargs)
        print()
        return res

    return wrapped


class Formatter:
    """An API to control formatting of the command line interface"""

    def __init__(self, width):
        self.w = width

    # style formatting options {'name': ('string code', length of string code)}
    formats = {
        "BLUE": ("\033[94m", 5),
        "GREEN": ("\033[92m", 5),
        "RED": ("\033[91m", 5),
        "BOLD": ("\033[1m", 4),
        "END": ("\033[0m", 4),
    }

    def center(self, msg, s=[], fill=" ", in_w=0, in_b="", fc=0, end="\n"):
        """Style text and center across width with optional inner container"""

        # n represents actual printed length of msg, less formatting characters
        n = len(msg) - fc

        # apply styles to message and inner container border
        fmt_start = ""
        for style in s:
            if style not in self.formats:
                raise NotImplementedError(f'Style "{style}" not implemented.')
            fmt_start += self.formats[style][0]
        msg = fmt_start + msg + self.formats["END"][0]

        # margin refers to combined space on each side of inner container
        margin = self.w - in_w if in_w else 0
        lmargin = margin // 2

        # padding refers to combined space on each side of msg inside container
        padding = self.w - margin - n - 2 * len(in_b)
        lpad = padding // 2
        # right padding only needed if fill is not ' ' or for inner container
        rpad = 0
        if in_w or fill != " ":
            rpad = lpad if padding % 2 == 0 else lpad + 1

        # print left margin, border, left padding, msg, right padding, border
        disp = " " * lmargin + in_b + fill * lpad + msg + fill * rpad + in_b
        print(disp, end=end)

    def apply(self, text, options=["BOLD"]):
        """Return string with formatting applied and number of format chars"""
        fmt_start = ""
        fmt_chars = 0
        for format in options:
            if format not in self.formats:
                raise NotImplementedError(f'Style "{format}" not implemented.')
            fmt_start += self.formats[format][0]
            fmt_chars += self.formats[format][1]
        fmt_chars += self.formats["END"][1]
        return fmt_start + text + self.formats["END"][0], fmt_chars

    def prompt(self, msg):
        """Prompt the user, applying consistent formatting"""
        self.center((">> " + msg + " >>"), s=["RED"], fc=-1, end="")
        return input(" ")
