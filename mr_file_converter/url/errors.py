from mr_file_converter.base_error import FileConverterException


class InvalidURL(FileConverterException):

    def __init__(self, url: str, next_stage: int | None = None):

        super().__init__(
            next_stage=next_stage,
            error_message=f'The url {url} is not valid, please enter the url again.',
            should_reply_to_message_id=True
        )


class URLToFileConversionError(FileConverterException):

    def __init__(self, url: str, target_format: str, next_stage: int | None = None):
        super().__init__(
            next_stage=next_stage,
            error_message=f'Error when converting URL {url} to target file format {target_format}'
        )
