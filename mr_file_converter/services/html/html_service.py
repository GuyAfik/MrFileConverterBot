from contextlib import contextmanager
from typing import Generator

import html2text
import pdfkit
from html2image import Html2Image

from mr_file_converter.services.io.io_service import IOService


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
    def to_pdf(self, source_file_path: str, custom_file_name: str) -> Generator[str, None, None]:
        with self.io_service.create_temp_pdf_file(
            prefix=custom_file_name
        ) as pdf_file:
            pdfkit.from_file(source_file_path, pdf_file)
            yield pdf_file

    @contextmanager
    def to_png(self, source_file_path: str, custom_file_name: str) -> Generator[str, None, None]:
        yield self.html_to_image.screenshot(
            html_file=source_file_path,
            save_as=f'{custom_file_name}.png'
        )[0]
        self.io_service.remove_file(f'{custom_file_name}.png')

    @contextmanager
    def to_jpg(self, source_file_path: str, custom_file_name: str) -> Generator[str, None, None]:
        yield self.html_to_image.screenshot(
            html_file=source_file_path, save_as=f'{custom_file_name}.jpg'
        )[0]
        self.io_service.remove_file(f'{custom_file_name}.jpg')

    @contextmanager
    def to_text(self, source_file_path: str, custom_file_name: str) -> Generator[str, None, None]:
        with self.io_service.create_temp_txt_file(
            prefix=custom_file_name
        ) as text_file:
            self.io_service.write_data_to_file(
                data=html2text.html2text(
                    self.io_service.read_file(file_path=source_file_path)
                ),
                file_path=text_file
            )
            yield text_file
