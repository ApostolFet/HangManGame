import sys
import os


_CURSOR_UP = "\x1b[A"
_ERASE_LINE = "\x1b[K"


def clear_line(n: int):
    for _ in range(n):
        sys.stdout.write(_CURSOR_UP)
        sys.stdout.write(_ERASE_LINE)


def clear():
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Linux and MacOS
        os.system("clear")
