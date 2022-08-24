TAB = '\t'
ENDLINE = '\n'
BREAK_LENGTH = 72
BREAK = '-' * BREAK_LENGTH

def break_padded(text: str) -> str:
    return padded(f"< {text} >", '-', BREAK_LENGTH)

def padded(text: str, pad_symbol: str, length: int) -> str:
    result = text
    l = len(text)
    while l < length:
        result = pad_symbol + result + pad_symbol
        l += 2 * len(pad_symbol)
    return result