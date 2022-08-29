class BotError(RuntimeError):
    def __init__(self, *args):
        super(BotError, self).__init__(*args)

class CommandInterruption(BotError):
    def __init__(self, *args):
        super(CommandInterruption, self).__init__(*args)

class ArgumentError(CommandInterruption):
    def __init__(self, *args):
        super(ArgumentError, self).__init__(*args)

class CloudFileNotFoundError(CommandInterruption):
    def __init__(self, *args):
        super(CloudFileNotFoundError, self).__init__(*args)

class DataDownloadError(CommandInterruption):
    def __init__(self, *args):
        super(DataDownloadError, self).__init__(*args)

class TestsFailedError(BotError):
    def __init__(self, *args):
        super(TestsFailedError, self).__init__(*args)


