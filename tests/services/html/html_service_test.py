import os.path

import pytest

from mr_file_converter.services.html.html_service import HTMLService
from mr_file_converter.services.io.io_service import IOService


@pytest.fixture()
def html_test_data_base_path(base_file_path):
    return f'{base_file_path}/services/html/test_data'


def test_html_to_pdf(html_service: HTMLService, html_test_data_base_path: str):
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
        source_file_path=f'{html_test_data_base_path}/test.html',
        custom_file_name='test'
    ) as pdf_file:
        assert os.path.exists(pdf_file)
        assert pdf_file == 'test.pdf'


def test_html_to_png(html_service: HTMLService, html_test_data_base_path: str):
    """
    Given:
     - test html file
     - custom file name.

    When:
     - converting a html file into photo file.

    Then:
     - make sure the newly created photo file exist in the file system
    """
    with html_service.to_png(
        source_file_path=f'{html_test_data_base_path}/test.html',
        custom_file_name='test'
    ) as png_file:
        assert os.path.exists(png_file)


def test_html_to_jpg(html_service: HTMLService, html_test_data_base_path: str):
    """
    Given:
     - test html file
     - custom file name.

    When:
     - converting a html file into jpg file.

    Then:
     - make sure the newly created jpg file exist in the file system
    """
    with html_service.to_jpg(
        source_file_path=f'{html_test_data_base_path}/test.html',
        custom_file_name='test'
    ) as jpg_file:
        assert os.path.exists(jpg_file)


def test_html_to_text(html_service: HTMLService, io_service: IOService, html_test_data_base_path: str):
    """
   Given:
    - test html file
    - custom file name.

   When:
    - converting a html file into text file.

   Then:
    - make sure the newly created text file exist in the file system
    - make sure it is possible to read the text file
   """
    with html_service.to_text(
        source_file_path=f'{html_test_data_base_path}/test.html',
        custom_file_name='test'
    ) as text_file:
        assert os.path.exists(text_file)
        assert io_service.read_file(text_file)
