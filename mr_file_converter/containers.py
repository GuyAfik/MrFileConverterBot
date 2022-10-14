import os

from dependency_injector import containers, providers
from telegram.ext import Updater

from mr_file_converter.command.command_service import CommandService
from mr_file_converter.converters import JsonConverter, YamlConverter
from mr_file_converter.downloader.youtube_downloader_handler import \
    YoutubeDownloaderHandlers
from mr_file_converter.downloader.youtube_downloader_service import \
    YoutubeDownloaderService
from mr_file_converter.file.file_handler import FileHandlers
from mr_file_converter.file.file_service import FileService
from mr_file_converter.io.io_service import IOService
from mr_file_converter.json.json_service import JsonService
from mr_file_converter.telegram.telegram_service import TelegramService
from mr_file_converter.yaml.yaml_service import YamlService


class Core(containers.DeclarativeContainer):

    updater = providers.Resource(
        Updater,
        token=os.getenv('BOT_TOKEN'),
    )


class Services(containers.DeclarativeContainer):
    core = providers.DependenciesContainer()
    telegram = providers.Factory(TelegramService, updater=core.updater)
    command = providers.Factory(CommandService, telegram_service=telegram)
    youtube_downloader = providers.Factory(
        YoutubeDownloaderService, telegram_service=telegram, command_service=command)

    # converters
    json_converter = providers.Factory(JsonConverter)
    yaml_converter = providers.Factory(YamlConverter)

    io = providers.Factory(IOService)
    json = providers.Factory(
        JsonService, command_service=command, io_service=io, json_converter=json_converter, yml_converter=yaml_converter
    )
    yaml = providers.Factory(
        YamlService, command_service=command, io_service=io, json_converter=json_converter, yml_converter=yaml_converter
    )
    file = providers.Factory(
        FileService,
        telegram_service=telegram,
        io_service=io,
        command_service=command,
        json_service=json,
        yaml_service=yaml
    )


class Handlers(containers.DeclarativeContainer):

    services = providers.DependenciesContainer()
    youtube_downloader = providers.Factory(
        YoutubeDownloaderHandlers, youtube_downloader_service=services.youtube_downloader
    )
    file = providers.Factory(
        FileHandlers, file_service=services.file
    )


class Application(containers.DeclarativeContainer):
    core = providers.Container(Core)
    services = providers.Container(Services, core=core)
    handlers = providers.Container(Handlers, services=services)
