class BotError(RuntimeError):
    def __init__(self, *args):
        super(BotError, self).__init__(*args)

class BotErrorWithStacktrace(RuntimeError):
    def __init__(self, *args):
        super(BotErrorWithStacktrace, self).__init__(*args)

class BotErrorWithoutStacktrace(RuntimeError):
    def __init__(self, *args):
        super(BotErrorWithoutStacktrace, self).__init__(*args)

class ArgumentError(BotErrorWithoutStacktrace):
    def __init__(self, *args):
        super(ArgumentError, self).__init__(*args)