import sys

import os

TAB = '\t'
ENDLINE = '\n'
BREAK_LENGTH = 88
BREAK = '-' * BREAK_LENGTH


def supports_color():
    """
    Returns True if the running system's terminal supports color, and False
    otherwise.
    """
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty


if supports_color():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
else:
    HEADER = ''
    OKBLUE = ''
    OKCYAN = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = ''


def break_padded(text: str) -> str:
    return padded(f"< {text} >", '-', BREAK_LENGTH)


def padded(text: str, pad_symbol: str, length: int) -> str:
    result = text
    l = len(text)
    while l < length:
        result = pad_symbol + result + pad_symbol
        l += 2 * len(pad_symbol)
    return f'{BOLD}{result[:length]}{ENDC}'


def formpath(path):
    return os.path.abspath(os.path.normpath(path))
