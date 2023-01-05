class AtfError(RuntimeError):
    def __init__(self, *args):
        super(AtfError, self).__init__(*args)


class NonInterruptingError(AtfError):
    def __init__(self, *args):
        super(NonInterruptingError, self).__init__(*args)


class ArgumentError(AtfError):
    def __init__(self, *args):
        super(ArgumentError, self).__init__(*args)


class NotFoundError(AtfError):
    def __init__(self, *args):
        super(NotFoundError, self).__init__(*args)


class DataDownloadError(AtfError):
    def __init__(self, *args):
        super(DataDownloadError, self).__init__(*args)


class TestsFailedError(AtfError):
    def __init__(self, *args):
        super(TestsFailedError, self).__init__(*args)


class CommandFailedError(AtfError):
    def __init__(self, *args):
        super(CommandFailedError, self).__init__(*args)


class InvalidDriveTypeError(AtfError):
    def __init__(self, *args):
        super(InvalidDriveTypeError, self).__init__(*args)


class IncompatibleDatasetsError(AtfError):
    def __init__(self, *args):
        super(IncompatibleDatasetsError, self).__init__(*args)


class SubmissionError(AtfError):
    def __init__(self, *args):
        super(SubmissionError, self).__init__(*args)


class DatasetValidationError(AtfError):
    def __init__(self, *args):
        super(DatasetValidationError, self).__init__(*args)
