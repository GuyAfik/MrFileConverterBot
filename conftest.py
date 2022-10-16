import pytest

from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.io.io_service import IOService


@pytest.fixture()
def io_service():
    return IOService()


@pytest.fixture()
def json_converter():
    return JsonConverter()


@pytest.fixture()
def xml_converter():
    return XMLConverter()


@pytest.fixture()
def yaml_converter():
    return YamlConverter()
