from typing import cast
from unittest.mock import MagicMock

import pytest
from telegram import Update
from telegram.ext import CallbackContext, Updater

from mr_file_converter.command.command_service import CommandService
from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.file.file_service import FileService
from mr_file_converter.html.html_service import HTMLService
from mr_file_converter.io.io_service import IOService
from mr_file_converter.json.json_service import JsonService
from mr_file_converter.telegram.telegram_service import TelegramService
from mr_file_converter.xml.xml_service import XMLService
from mr_file_converter.yaml.yaml_service import YamlService

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
def file_service(
    telegram_service: TelegramService,
    io_service: IOService,
    command_service: CommandService,
    json_service: JsonService,
    yml_service: YamlService,
    xml_service: XMLService,
    html_service: HTMLService
) -> FileService:
    return FileService(
        telegram_service=telegram_service,
        io_service=io_service,
        command_service=command_service,
        json_service=json_service,
        yaml_service=yml_service,
        xml_service=xml_service,
        html_service=html_service
    )


@pytest.fixture()
def telegram_context() -> CallbackContext:
    context = cast(CallbackContext, MagicMock())
    context.user_data = {}
    return context
