import os.path

import pytest

from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.io.io_service import IOService
from mr_file_converter.yaml.yaml_service import YamlService


@pytest.fixture()
def yml_service(
    io_service: IOService,
    json_converter: JsonConverter,
    yaml_converter: YamlConverter,
    xml_converter: XMLConverter
) -> YamlService:
    return YamlService(
        io_service=io_service,
        json_converter=json_converter,
        yml_converter=yaml_converter,
        xml_converter=xml_converter
    )


def test_yml_to_json(yml_service: YamlService, base_file_path: str):
    """
    Given:
     - test YML file
     - custom file name.

    When:
     - converting a YML file into a JSON file.

    Then:
     - make sure the newly created JSON file exist in the file system
     - make sure the name is correct
     - make sure it's possible to read the JSON file after it has been converted.
    """
    with yml_service.to_json(
        source_file_path=f'{base_file_path}/yaml/test_data/test.yml',
        custom_file_name='test'
    ) as json_file:
        assert os.path.exists(json_file)
        assert json_file == 'test.json'
        assert yml_service.json_converter.read(json_file)


def test_yml_to_xml(yml_service: YamlService, base_file_path: str):
    """
    Given:
     - test yml file
     - custom file name.

    When:
     - converting a YML file into XML file.

    Then:
     - make sure the newly created XML file exist in the file system
     - make sure the name is correct
     - make sure it's possible to read the XML file after it has been converted.
    """
    with yml_service.to_xml(
        source_file_path=f'{base_file_path}/yaml/test_data/test.yml',
        custom_file_name='test'
    ) as xml_file:
        assert os.path.exists(xml_file)
        assert xml_file == 'test.xml'
        assert yml_service.xml_converter.read(xml_file)


def test_yml_to_text(yml_service: YamlService, base_file_path: str):
    """
    Given:
     - test YML file
     - custom file name.

    When:
     - converting a YML file into text file.

    Then:
     - make sure the newly created text file exist in the file system
     - make sure the name is correct
    """
    with yml_service.to_text(
        source_file_path=f'{base_file_path}/yaml/test_data/test.yml',
        custom_file_name='test'
    ) as text_file:
        assert os.path.exists(text_file)
        assert text_file == 'test.txt'
