

class FileConverterException(Exception):
    """
    Base error for every error that MrFileConverter encounters
    """

    def __init__(
            self, next_stage: int | None = None, error_message: str = '', should_reply_to_message_id: bool = False
    ):
        self.next_stage = next_stage
        self.should_reply_to_message_id = should_reply_to_message_id
        super().__init__(error_message)
