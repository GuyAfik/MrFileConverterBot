import os

import pytest

from mr_file_converter.services.photo.photo_service import PhotoService


@pytest.fixture()
def photo_test_data_base_path(base_file_path) -> str:
    return f'{base_file_path}/services/photo/test_data'


@pytest.mark.parametrize(
    'file_name',
    [
        'test.png',
        'test.jpg'
    ]
)
def test_photo_to_pdf(photo_service: PhotoService, photo_test_data_base_path: str, file_name: str):
    """
    Given:
     - test photo file (png, jpg)
     - custom file name.

    When:
     - converting a photo file into a pdf file.

    Then:
     - make sure the newly created pdf file exist in the file system
     - make sure the name is correct
    """
    with photo_service.to_pdf(
        source_file_path=f'{photo_test_data_base_path}/{file_name}',
        custom_file_name='test'
    ) as pdf_file:
        assert os.path.exists(pdf_file)
        assert pdf_file == 'test.pdf'


def test_photo_to_text(photo_service: PhotoService, photo_test_data_base_path: str):
    """
    Given:
    - test photo file (jpg)
    - custom file name.

    When:
    - converting a photo file (with text inside) into a text file.

    Then:
    - make sure the newly created text file exist in the file system
    - make sure the name is correct
    - make sure the text content is correct
   """
    with photo_service.to_text(
        source_file_path=f'{photo_test_data_base_path}/test.jpg',
        custom_file_name='test'
    ) as text_file:
        assert os.path.exists(text_file)
        assert text_file == 'test.txt'
        with open(text_file, 'r') as file:
            assert file.read().strip() == 'Sample Text 1'
