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
     - make sure the name of the file is the correct.
    """
    with url_service.to_pdf(
        url='https://www.google.com/', custom_file_name='test'
    ) as pdf_file:
        assert os.path.exists(pdf_file)
        assert pdf_file == 'test.pdf'
