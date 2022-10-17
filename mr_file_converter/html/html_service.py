import os
from contextlib import contextmanager
from typing import Generator

import pdfkit
from html2image import Html2Image

from mr_file_converter.io.io_service import IOService


class HTMLService:
    """
    TODO: https://github.com/JazzCore/python-pdfkit - need to install wkhtmltopdf on the docker
    """

    def __init__(
        self,
        io_service: IOService
    ):
        self.io_service = io_service
        self.html_to_image = Html2Image()

    @contextmanager
    def to_pdf(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        with self.io_service.create_temp_pdf_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as pdf_file:
            pdfkit.from_file(source_file_path, pdf_file)
            yield pdf_file

    @contextmanager
    def to_png(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        with self.io_service.create_temp_png_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as png_file:
            self.html_to_image.screenshot(
                html_file=source_file_path, save_as=png_file
            )
            yield png_file

    @contextmanager
    def to_jpg(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        with self.io_service.create_temp_jpg_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as jpg_file:
            self.html_to_image.screenshot(
                html_file=source_file_path, save_as=jpg_file
            )
            yield jpg_file
