from typing import cast
from unittest.mock import MagicMock

import pytest
from telegram import Update
from telegram.ext import CallbackContext, Updater

from mr_file_converter.command.command_service import CommandService
from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.io.io_service import IOService
from mr_file_converter.telegram.telegram_service import TelegramService

BASE_PATH = '../tests'


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
def telegram_context() -> CallbackContext:
    context = cast(CallbackContext, MagicMock())
    context.user_data = {}
    return context
