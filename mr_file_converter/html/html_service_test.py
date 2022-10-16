import os.path

import pytest

from mr_file_converter.html.html_service import HTMLService
from mr_file_converter.io.io_service import IOService


@pytest.fixture()
def html_service(
    io_service: IOService
) -> HTMLService:
    return HTMLService(io_service=io_service)


def test_html_to_pdf(html_service: HTMLService, base_file_path: str):
    """
    Given:
     - test html file
     - custom file name.

    When:
     - converting a html file into a pdf file.

    Then:
     - make sure the newly created pdf file exist in the file system
     - make sure the name is correct
    """
    with html_service.to_pdf(
        source_file_path=f'{base_file_path}/html/test_data/test.html',
        custom_file_name='test'
    ) as pdf_file:
        assert os.path.exists(pdf_file)
        assert pdf_file == 'test.pdf'


def test_html_to_png(html_service: HTMLService, base_file_path: str):
    """
    Given:
     - test html file
     - custom file name.

    When:
     - converting a html file into png file.

    Then:
     - make sure the newly created png file exist in the file system
     - make sure the name is correct
    """
    with html_service.to_png(
        source_file_path=f'{base_file_path}/html/test_data/test.html',
        custom_file_name='test'
    ) as png_file:
        assert os.path.exists(png_file)
        assert png_file == 'test.png'
