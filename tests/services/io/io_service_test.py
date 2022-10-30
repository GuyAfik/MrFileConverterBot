import os.path

from mr_file_converter.services.io.io_service import IOService


def test_create_temp_file(io_service: IOService):
    """
    Given:
    - prefix and suffix = 'txt'

    When:
    - trying to create a temp file

    Then:
    - make sure the file exists in the file system
   """
    with io_service.create_temp_file(prefix='test', suffix='txt') as file_name:
        assert os.path.exists(file_name)
