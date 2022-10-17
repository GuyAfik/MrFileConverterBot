from mr_file_converter.base_error import FileConverterException


class FileTypeNotSupported(FileConverterException):

    def __init__(self, next_stage: int, _file_type: str):
        super().__init__(
            next_stage=next_stage,
            error_message=f'file is of type {_file_type} and is not supported at the moment'
        )


class FileConversionError(FileConverterException):

    def __init__(self, next_stage: int, source_format: str, target_format: str):
        super().__init__(
            next_stage=next_stage,
            error_message=f'Error when converting from source format {source_format} to target format {target_format}'
        )
