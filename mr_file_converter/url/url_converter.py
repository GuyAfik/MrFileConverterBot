from contextlib import contextmanager
from typing import Generator

import pdfkit

from mr_file_converter.io.io_service import IOService


class URLConverter:

    def __init__(
        self,
        io_service: IOService,
    ):
        self.io_service = io_service

    @contextmanager
    def to_pdf(self, url: str, custom_file_name: str) -> Generator[str, None, None]:
        with self.io_service.create_temp_pdf_file(prefix=custom_file_name) as pdf_file:
            pdfkit.from_url(url, pdf_file)
            yield pdf_file
