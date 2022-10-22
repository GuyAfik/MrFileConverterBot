import os.path

import pytest

from mr_file_converter.services.html.html_service import HTMLService


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
     - converting a html file into png file.

    Then:
     - make sure the newly created png file exist in the file system
     - make sure the name is correct
    """
    with html_service.to_png(
        source_file_path=f'{html_test_data_base_path}/test.html',
        custom_file_name='test'
    ) as png_file:
        assert os.path.exists(png_file)
        assert png_file == 'test.png'


def test_html_to_jpg(html_service: HTMLService, html_test_data_base_path: str):
    """
    Given:
     - test html file
     - custom file name.

    When:
     - converting a html file into jpg file.

    Then:
     - make sure the newly created jpg file exist in the file system
     - make sure the name is correct
    """
    with html_service.to_jpg(
        source_file_path=f'{html_test_data_base_path}/test.html',
        custom_file_name='test'
    ) as jpg_file:
        assert os.path.exists(jpg_file)
        assert jpg_file == 'test.jpg'