import sys
import os


def clear_line(n: int):
    _CURSOR_UP = "\x1b[A"
    _ERASE_LINE = "\x1b[K"

    for _ in range(n):
        sys.stdout.write(_CURSOR_UP)
        sys.stdout.write(_ERASE_LINE)


def clear():
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For Linux and MacOS
        os.system("clear")
