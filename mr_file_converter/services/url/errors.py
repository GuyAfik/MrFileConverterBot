from urllib.error import URLError

from mr_file_converter.base_error import FileConverterException


class InvalidURL(FileConverterException):

    def __init__(
        self,
        url: str,
        next_stage: int | None = None,
        exception: Exception | None = None
    ):
        if isinstance(exception, (ValueError, URLError)):
            error_message = f'the url {url} is invalid, please enter a valid url'
        else:  # means we got an HttpError such as <HTTPError 403: 'Forbidden'>
            error_message = f'Unable to read {url}, please try a different url'
        super().__init__(
            original_exception=exception,
            next_stage=next_stage,
            error_message=error_message,
            should_reply_to_message_id=True
        )


class URLToFileConversionError(FileConverterException):

    def __init__(
        self,
        url: str,
        target_format: str,
        next_stage: int | None = None,
        original_exception: Exception | None = None
    ):
        super().__init__(
            original_exception=original_exception,
            next_stage=next_stage,
            error_message=f'Error when converting URL {url} to target file format {target_format}'
        )
