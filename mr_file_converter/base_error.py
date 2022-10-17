

class FileConverterException(Exception):
    """
    Base error for every error that MrFileConverter encounters
    """

    def __init__(self, next_stage: int | None = None, error_message: str = ''):
        self.next_stage = next_stage
        super().__init__(error_message)
