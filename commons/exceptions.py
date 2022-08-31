class BotError(RuntimeError):
    def __init__(self, *args):
        super(BotError, self).__init__(*args)

class NotInterruptingError(BotError):
    def __init__(self, *args):
        super(NotInterruptingError, self).__init__(*args)

class ArgumentError(BotError):
    def __init__(self, *args):
        super(ArgumentError, self).__init__(*args)

class CloudFileNotFoundError(BotError):
    def __init__(self, *args):
        super(CloudFileNotFoundError, self).__init__(*args)

class DataDownloadError(BotError):
    def __init__(self, *args):
        super(DataDownloadError, self).__init__(*args)

class TestsFailedError(NotInterruptingError):
    def __init__(self, *args):
        super(TestsFailedError, self).__init__(*args)


