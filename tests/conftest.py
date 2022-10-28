from typing import cast
from unittest.mock import MagicMock

import pytest
from telegram import Update
from telegram.ext import CallbackContext, Updater

from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.services.command.command_service import CommandService
from mr_file_converter.services.html.html_service import HTMLService
from mr_file_converter.services.io.io_service import IOService
from mr_file_converter.services.json.json_service import JsonService
from mr_file_converter.services.pdf.pdf_service import PdfService
from mr_file_converter.services.png.png_service import PngService
from mr_file_converter.services.telegram.telegram_service import \
    TelegramService
from mr_file_converter.services.url.url_service import URLService
from mr_file_converter.services.xml.xml_service import XMLService
from mr_file_converter.services.yaml.yaml_service import YamlService

BASE_PATH = 'tests'


@pytest.fixture()
def updater() -> Updater:
    return cast(Updater, MagicMock())


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


@pytest.fixture()
def command_service() -> CommandService:
    return cast(CommandService, MagicMock())


@pytest.fixture()
def telegram_service(updater: MagicMock) -> TelegramService:
    return TelegramService(updater=updater)


@pytest.fixture()
def telegram_update() -> Update:
    return cast(Update, MagicMock())


@pytest.fixture()
def html_service(
    io_service: IOService
) -> HTMLService:
    return HTMLService(io_service=io_service)


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


@pytest.fixture()
def telegram_context() -> CallbackContext:
    context = cast(CallbackContext, MagicMock())
    context.user_data = {}
    return context


@pytest.fixture()
def url_service(
    io_service: IOService
) -> URLService:
    return URLService(io_service=io_service)


@pytest.fixture()
def pdf_service(
    io_service: IOService
) -> PdfService:
    return PdfService(io_service=io_service)


@pytest.fixture()
def png_service(
    io_service: IOService
) -> PngService:
    return PngService(io_service=io_service)
