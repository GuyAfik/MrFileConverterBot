import os
from contextlib import contextmanager
from typing import Generator

from mr_file_converter.services.io.io_service import IOService
import pdf2docx


class PdfService:

    def __init__(
        self,
        io_service: IOService
    ):
        self.io_service = io_service

    @contextmanager
    def to_docx(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        with self.io_service.create_temp_docx_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as docx_file:
            pdf2docx.parse(source_file_path, docx_file)
            yield docx_file