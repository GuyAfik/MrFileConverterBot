import os.path

import pytest

from mr_file_converter.services.xml.xml_service import XMLService


@pytest.fixture()
def xml_test_data_base_path(base_file_path):
    return f'{base_file_path}/services/xml/test_data'


def test_xml_to_json(xml_service: XMLService, xml_test_data_base_path: str):
    """
    Given:
     - test XML file
     - custom file name.

    When:
     - converting XML file into a json file.

    Then:
     - make sure the newly created JSON file exist in the file system
     - make sure it's possible to read the JSON file after it has been converted.
    """
    with xml_service.to_json(
        source_file_path=f'{xml_test_data_base_path}/test.xml',
        custom_file_name='test'
    ) as json_file:
        assert os.path.exists(json_file)
        assert xml_service.json_converter.read(json_file)


def test_xml_to_yml(xml_service: XMLService, xml_test_data_base_path: str):
    """
    Given:
     - test XML file
     - custom file name.

    When:
     - converting XML file into a yml file.

    Then:
     - make sure the newly created YML file exist in the file system
     - make sure it's possible to read the YML file after it has been converted.
    """
    with xml_service.to_yml(
        source_file_path=f'{xml_test_data_base_path}/test.xml',
        custom_file_name='test'
    ) as yml_file:
        assert os.path.exists(yml_file)
        assert xml_service.yml_converter.read(yml_file)
