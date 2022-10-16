import os.path

import pytest

from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.io.io_service import IOService
from mr_file_converter.xml.xml_service import XMLService


@pytest.fixture()
def xml_service(
    io_service: IOService,
    json_converter: JsonConverter,
    yaml_converter: YamlConverter,
    xml_converter: XMLConverter
) -> XMLService:
    return XMLService(
        io_service=io_service,
        json_converter=json_converter,
        yml_converter=yaml_converter,
        xml_converter=xml_converter
    )


@pytest.fixture()
def xml_test_data_base_path(base_file_path):
    return f'{base_file_path}/xml/test_data'


def test_xml_to_json(xml_service: XMLService, xml_test_data_base_path: str):
    """
    Given:
     - test XML file
     - custom file name.

    When:
     - converting XML file into a json file.

    Then:
     - make sure the newly created JSON file exist in the file system
     - make sure the name is correct
     - make sure it's possible to read the JSON file after it has been converted.
    """
    with xml_service.to_json(
        source_file_path=f'{xml_test_data_base_path}/test.xml',
        custom_file_name='test'
    ) as json_file:
        assert os.path.exists(json_file)
        assert json_file == 'test.json'
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
     - make sure the name is correct
     - make sure it's possible to read the YML file after it has been converted.
    """
    with xml_service.to_yml(
        source_file_path=f'{xml_test_data_base_path}/test.xml',
        custom_file_name='test'
    ) as yml_file:
        assert os.path.exists(yml_file)
        assert yml_file == 'test.yml'
        assert xml_service.yml_converter.read(yml_file)
