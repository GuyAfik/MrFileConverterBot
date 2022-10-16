import os
from contextlib import contextmanager
from typing import Generator

import pdfkit

from mr_file_converter.command.command_service import CommandService
from mr_file_converter.io.io_service import IOService


class HTMLService:
    """
    TODO: https://github.com/JazzCore/python-pdfkit - need to install wkhtmltopdf on the docker
    TODO: brew install homebrew/cask/wkhtmltopdf
    """
    def __init__(
        self,
        command_service: CommandService,
        io_service: IOService
    ):
        self.command_service = command_service
        self.io_service = io_service

    @contextmanager
    def to_pdf(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        with self.io_service.create_temp_pdf_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as pdf_file:
            pdfkit.from_file(source_file_path, pdf_file)
            yield pdf_file
