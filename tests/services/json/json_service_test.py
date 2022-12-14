import os.path

import pytest

from mr_file_converter.services.json.json_service import JsonService


@pytest.fixture()
def json_test_data_base_path(base_file_path):
    return f'{base_file_path}/services/json/test_data'


def test_json_to_yml(json_service: JsonService, json_test_data_base_path: str):
    """
    Given:
     - test json file
     - custom file name.

    When:
     - converting a json file into a yml file.

    Then:
     - make sure the newly created yml file exist in the file system
     - make sure it's possible to read the yml file after it has been converted.
    """
    with json_service.to_yml(
        source_file_path=f'{json_test_data_base_path}/test.json',
        custom_file_name='test'
    ) as yml_file:
        assert os.path.exists(yml_file)
        assert json_service.yml_converter.read(yml_file)


def test_json_to_xml(json_service: JsonService, json_test_data_base_path: str):
    """
    Given:
     - test json file
     - custom file name.

    When:
     - converting a json file into XML file.

    Then:
     - make sure the newly created XML file exist in the file system
     - make sure it's possible to read the XML file after it has been converted.
    """
    with json_service.to_xml(
        source_file_path=f'{json_test_data_base_path}/test.json',
        custom_file_name='test'
    ) as xml_file:
        assert os.path.exists(xml_file)
        assert json_service.xml_converter.read(xml_file)


def test_json_to_text(json_service: JsonService, json_test_data_base_path: str):
    """
    Given:
     - test json file
     - custom file name.

    When:
     - converting a json file into text file.

    Then:
     - make sure the newly created text file exist in the file system
    """
    with json_service.to_text(
        source_file_path=f'{json_test_data_base_path}/test.json',
        custom_file_name='test'
    ) as text_file:
        assert os.path.exists(text_file)
