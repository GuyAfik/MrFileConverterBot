import os.path

import pytest

from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.io.io_service import IOService
from mr_file_converter.json.json_service import JsonService


@pytest.fixture()
def json_service(
    io_service: IOService,
    json_converter: JsonConverter,
    yaml_converter: YamlConverter,
    xml_converter: XMLConverter
) -> JsonService:
    return JsonService(
        io_service=io_service,
        json_converter=json_converter,
        yml_converter=yaml_converter,
        xml_converter=xml_converter
    )


def test_json_to_yml(json_service: JsonService):
    """
    Given:
     - test json file
     - custom file name.

    When:
     - converting a json file into a yml file.

    Then:
     - make sure the newly created yml file exist in the file system
     - make sure the name is correct
     - make sure it's possible to read the yml file after it has been converted.
    """
    with json_service.to_yml(
        source_file_path='mr_file_converter/json/test_data/test.json',
        custom_file_name='test'
    ) as yml_file:
        assert os.path.exists(yml_file)
        assert yml_file == 'test.yml'
        assert json_service.yml_converter.read(yml_file)


def test_json_to_xml(json_service: JsonService):
    """
    Given:
     - test json file
     - custom file name.

    When:
     - converting a json file into XML file.

    Then:
     - make sure the newly created XML file exist in the file system
     - make sure the name is correct
     - make sure it's possible to read the XML file after it has been converted.
    """
    with json_service.to_xml(
        source_file_path='mr_file_converter/json/test_data/test.json',
        custom_file_name='test'
    ) as xml_file:
        assert os.path.exists(xml_file)
        assert xml_file == 'test.xml'
        assert json_service.xml_converter.read(xml_file)


def test_json_to_text(json_service: JsonService):
    """
    Given:
     - test json file
     - custom file name.

    When:
     - converting a json file into text file.

    Then:
     - make sure the newly created text file exist in the file system
     - make sure the name is correct
    """
    with json_service.to_text(
        source_file_path='mr_file_converter/json/test_data/test.json',
        custom_file_name='test'
    ) as text_file:
        assert os.path.exists(text_file)
        assert text_file == 'test.txt'
