from commons.env import getenv
import os

TAB = '\t'
ENDLINE = '\n'
BREAK_LENGTH = 72
BREAK = '-' * BREAK_LENGTH
if getenv('COLOR_OUTPUT') is not None and getenv(
        'COLOR_OUTPUT').lower() == "true":
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
