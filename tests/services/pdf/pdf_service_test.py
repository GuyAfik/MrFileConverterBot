import os

import pytest

from mr_file_converter.services.pdf.pdf_service import PdfService


@pytest.fixture()
def pdf_test_data_base_path(base_file_path) -> str:
    return f'{base_file_path}/services/pdf/test_data'


def test_pdf_to_docx(pdf_service: PdfService, pdf_test_data_base_path: str):
    """
    Given:
     - test pdf file (with 2 pages - only text)
     - custom file name.

    When:
     - converting a pdf file into a docx file.

    Then:
     - make sure the newly created docx file exist in the file system
     - make sure the name is correct
    """
    with pdf_service.to_docx(
        source_file_path=f'{pdf_test_data_base_path}/test.pdf',
        custom_file_name='test'
    ) as pdf_file:
        assert os.path.exists(pdf_file)
        assert pdf_file == 'test.docx'
