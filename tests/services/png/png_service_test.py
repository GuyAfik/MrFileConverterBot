import os

from mr_file_converter.services.png.png_service import PngService

import pytest


@pytest.fixture()
def png_test_data_base_path(base_file_path) -> str:
    return f'{base_file_path}/services/png/test_data'


def test_png_to_pdf(png_service: PngService, png_test_data_base_path: str):
    """
    Given:
     - test png file
     - custom file name.

    When:
     - converting a png file into a pdf file.

    Then:
     - make sure the newly created pdf file exist in the file system
     - make sure the name is correct
    """
    with png_service.to_pdf(
        source_file_path=f'{png_test_data_base_path}/test.png',
        custom_file_name='test'
    ) as png_file:
        assert os.path.exists(png_file)
        assert png_file == 'test.pdf'
