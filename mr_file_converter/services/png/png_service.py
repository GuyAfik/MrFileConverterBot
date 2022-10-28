import os
from contextlib import contextmanager
from typing import Generator

import img2pdf

from mr_file_converter.services.io.io_service import IOService


class PngService:

    def __init__(
        self,
        io_service: IOService
    ):
        self.io_service = io_service

    @contextmanager
    def to_pdf(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        with self.io_service.create_temp_pdf_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as pdf_file:
            pdf_bytes = img2pdf.convert(source_file_path)
            self.io_service.write_data_to_file(
                data=pdf_bytes, file_path=pdf_file, mode='wb')
            yield pdf_file
