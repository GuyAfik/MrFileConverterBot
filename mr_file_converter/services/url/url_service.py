from contextlib import contextmanager
from typing import Generator
from urllib.request import urlopen

import imgkit
import pdfkit
from bs4 import BeautifulSoup

from mr_file_converter.services.io.io_service import IOService


class URLService:

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

    @contextmanager
    def to_html(self, url: str, custom_file_name: str) -> Generator[str, None, None]:
        with self.io_service.create_temp_html_file(
            prefix=custom_file_name
        ) as html_file:
            bs = BeautifulSoup(urlopen(url).read(), 'html.parser')
            self.io_service.write_data_to_file(
                data=bs.prettify(), file_path=html_file)
            yield html_file

    @contextmanager
    def to_png(self, url: str, custom_file_name: str) -> Generator[str, None, None]:
        with self.io_service.create_temp_png_file(
            prefix=custom_file_name
        ) as png_file:
            imgkit.from_url(url, png_file)
            yield png_file

    @contextmanager
    def to_jpg(self, url: str, custom_file_name: str) -> Generator[str, None, None]:
        with self.io_service.create_temp_jpg_file(
            prefix=custom_file_name
        ) as jpg_file:
            imgkit.from_url(url, jpg_file)
            yield jpg_file
