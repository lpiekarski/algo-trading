class BotError(RuntimeError):
    def __init__(self, *args):
        super(BotError, self).__init__(*args)

class ArgumentError(BotError):
    def __init__(self, *args):
        super(ArgumentError, self).__init__(*args)

class CloudFileNotFoundError(BotError):
    def __init__(self, *args):
        super(CloudFileNotFoundError, self).__init__(*args)

class DataDownloadError(BotError):
    def __init__(self, *args):
        super(DataDownloadError, self).__init__(*args)