import os

from dependency_injector import containers, providers
from telegram.ext import Updater

from mr_file_converter.conversations.file.file_conversation import \
    FileConversation
from mr_file_converter.conversations.file.file_handler import FileHandlers
from mr_file_converter.conversations.url.url_conversation import \
    URLConversation
from mr_file_converter.conversations.url.url_handler import URLHandlers
from mr_file_converter.conversations.youtube.youtube_downloader_conversation import \
    YoutubeDownloaderConversation
from mr_file_converter.conversations.youtube.youtube_downloader_handler import \
    YoutubeDownloaderHandlers
from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.services.command.command_service import CommandService
from mr_file_converter.services.html.html_service import HTMLService
from mr_file_converter.services.io.io_service import IOService
from mr_file_converter.services.json.json_service import JsonService
from mr_file_converter.services.pdf.pdf_service import PdfService
from mr_file_converter.services.telegram.telegram_service import \
    TelegramService
from mr_file_converter.services.url.url_service import URLService
from mr_file_converter.services.xml.xml_service import XMLService
from mr_file_converter.services.yaml.yaml_service import YamlService


class Core(containers.DeclarativeContainer):

    updater = providers.Resource(
        Updater,
        token=os.getenv('BOT_TOKEN'),
    )


class Converters(containers.DeclarativeContainer):
    json = providers.Factory(JsonConverter)
    yaml = providers.Factory(YamlConverter)
    xml = providers.Factory(XMLConverter)


class Services(containers.DeclarativeContainer):
    core = providers.DependenciesContainer()
    converters = providers.DependenciesContainer()

    telegram = providers.Factory(TelegramService, updater=core.updater)
    io = providers.Factory(IOService)
    command = providers.Factory(
        CommandService, telegram_service=telegram, io_service=io
    )

    json = providers.Factory(
        JsonService,
        io_service=io,
        json_converter=converters.json,
        yml_converter=converters.yaml,
        xml_converter=converters.xml
    )
    yaml = providers.Factory(
        YamlService,
        io_service=io,
        json_converter=converters.json,
        yml_converter=converters.yaml,
        xml_converter=converters.xml
    )
    xml = providers.Factory(
        XMLService,
        io_service=io,
        json_converter=converters.json,
        yml_converter=converters.yaml,
        xml_converter=converters.xml
    )
    html = providers.Factory(
        HTMLService,
        io_service=io
    )
    pdf = providers.Factory(
        PdfService,
        io_service=io
    )
    url = providers.Factory(URLService, io_service=io)


class Conversations(containers.DeclarativeContainer):
    services = providers.DependenciesContainer()
    youtube_downloader = providers.Factory(
        YoutubeDownloaderConversation, telegram_service=services.telegram
    )
    url = providers.Factory(
        URLConversation,
        telegram_service=services.telegram,
        url_service=services.url
    )

    file = providers.Factory(
        FileConversation,
        telegram_service=services.telegram,
        io_service=services.io,
        json_service=services.json,
        yaml_service=services.yaml,
        xml_service=services.xml,
        html_service=services.html,
        pdf_service=services.pdf
    )


class Handlers(containers.DeclarativeContainer):
    services = providers.DependenciesContainer()
    conversations = providers.DependenciesContainer()

    youtube_downloader = providers.Factory(
        YoutubeDownloaderHandlers,
        youtube_downloader_conversation=conversations.youtube_downloader,
        command_service=services.command
    )
    file = providers.Factory(
        FileHandlers, file_conversation=conversations.file, command_service=services.command
    )
    url = providers.Factory(
        URLHandlers, url_conversation=conversations.url, command_service=services.command
    )


class Application(containers.DeclarativeContainer):
    core = providers.Container(Core)
    converters = providers.Container(Converters)
    services = providers.Container(Services, core=core, converters=converters)
    conversations = providers.Container(Conversations, services=services)
    handlers = providers.Container(
        Handlers, conversations=conversations, services=services)
