import os

from mr_file_converter.services.url.url_service import URLService


def test_url_to_pdf(url_service: URLService):
    """
    Given:
     - google URL.
     - custom file name.

    When:
     - converting url into a pdf file

    Then:
     - make sure the file creation succeeds and that the file exists.
    """
    with url_service.to_pdf(
        url='https://www.google.com/', custom_file_name='test'
    ) as pdf_file:
        assert os.path.exists(pdf_file)
        assert pdf_file == 'test.pdf'


def test_url_to_html(url_service: URLService):
    """
    Given:
     - google URL.
     - custom file name.

    When:
     - converting url into a html file

    Then:
     - make sure the file creation succeeds and that the file exists.
    """
    with url_service.to_html(
        url='https://www.google.com/', custom_file_name='test'
    ) as html_file:
        assert os.path.exists(html_file)


def test_url_to_png(url_service: URLService):
    """
    Given:
     - google URL.
     - custom file name.

    When:
     - converting url into a photo file

    Then:
     - make sure the file creation succeeds and that the file exists.
    """
    with url_service.to_png(
        url='https://www.google.com/', custom_file_name='test'
    ) as png_file:
        assert os.path.exists(png_file)


def test_url_to_jpg(url_service: URLService):
    """
    Given:
     - google URL.
     - custom file name.

    When:
     - converting url into a jpg file

    Then:
     - make sure the file creation succeeds and that the file exists.
    """
    with url_service.to_jpg(
        url='https://www.google.com/', custom_file_name='test'
    ) as jpg_file:
        assert os.path.exists(jpg_file)
        assert jpg_file == 'test.jpg'
