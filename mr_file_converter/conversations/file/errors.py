from mr_file_converter.base_error import FileConverterException


class FileTypeNotSupported(FileConverterException):

    def __init__(self, _file_type: str, next_stage: int | None = None):
        super().__init__(
            next_stage=next_stage,
            error_message=f'file is of type {_file_type} and is not supported at the moment'
        )


class FileConversionError(FileConverterException):

    def __init__(self, source_format: str, target_format: str, next_stage: int | None = None):
        super().__init__(
            next_stage=next_stage,
            error_message=f'Error when converting from source format {source_format} to target format {target_format}'
        )
