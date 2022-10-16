import pytest

from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.io.io_service import IOService

BASE_PATH = 'mr_file_converter'


@pytest.fixture()
def io_service() -> IOService:
    return IOService()


@pytest.fixture()
def json_converter() -> JsonConverter:
    return JsonConverter()


@pytest.fixture()
def xml_converter() -> XMLConverter:
    return XMLConverter()


@pytest.fixture()
def yaml_converter() -> YamlConverter:
    return YamlConverter()


@pytest.fixture()
def base_file_path() -> str:
    return BASE_PATH
