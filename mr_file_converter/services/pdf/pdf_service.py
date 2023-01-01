from contextlib import contextmanager
from typing import Generator

import pdf2docx
import PyPDF2

from mr_file_converter.services.io.io_service import IOService


class PdfService:

    def __init__(
        self,
        io_service: IOService
    ):
        self.io_service = io_service

    @contextmanager
    def to_docx(self, source_file_path: str, custom_file_name: str) -> Generator[str, None, None]:
        with self.io_service.create_temp_docx_file(
            prefix=custom_file_name
        ) as docx_file:
            pdf2docx.parse(source_file_path, docx_file)
            yield docx_file

    @contextmanager
    def to_txt(self, source_file_path: str, custom_file_name: str) -> Generator[str, None, None]:
        with self.io_service.create_temp_txt_file(
            prefix=custom_file_name
        ) as txt_file:
            with open(source_file_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                pdf_text_content = '\n'.join(
                    page.extractText() for page in pdf_reader.pages
                )
                self.io_service.write_data_to_file(
                    data=pdf_text_content, file_path=txt_file
                )
                yield txt_file
