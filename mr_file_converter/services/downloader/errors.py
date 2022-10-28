from mr_file_converter.base_error import FileConverterException


class InvalidYouTubeURL(FileConverterException):
    """
    Raised when a user provided an invalid YouTube URL to download.
    """

    def __init__(
        self,
        url: str,
        next_stage: int | None = None,
        original_exception: Exception | None = None
    ):
        super().__init__(
            original_exception=original_exception,
            next_stage=next_stage,
            error_message=f'URL {url} is not a valid YouTube video, Please enter again a valid URL',
            should_reply_to_message_id=True
        )


class YouTubeVideoDownloadError(FileConverterException):
    """
    Raised when there was an error when downloading the YouTube video.
    """

    def __init__(
        self,
        url: str,
        _format: str,
        next_stage: int | None = None,
        original_exception: Exception | None = None
    ):
        super().__init__(
            original_exception=original_exception,
            next_stage=next_stage,
            error_message=f'Failed to download YouTube video {url} as {_format}',
        )
