import os

from dependency_injector import containers, providers
from telegram.ext import Updater

from mr_file_converter.downloader.youtube_downloader_handler import \
    YoutubeDownloaderHandlers
from mr_file_converter.downloader.youtube_downloader_service import \
    YoutubeDownloaderService
from mr_file_converter.telegram.telegram_service import TelegramService


class Core(containers.DeclarativeContainer):

    updater = providers.Resource(
        Updater,
        token=os.getenv('BOT_TOKEN'),
    )


class Services(containers.DeclarativeContainer):
    core = providers.DependenciesContainer()
    telegram = providers.Factory(TelegramService, updater=core.updater)
    youtube_downloader = providers.Factory(
        YoutubeDownloaderService, telegram_service=telegram)


class Handlers(containers.DeclarativeContainer):

    services = providers.DependenciesContainer()
    youtube_downloader = providers.Factory(
        YoutubeDownloaderHandlers, youtube_downloader_service=services.youtube_downloader
    )


class Application(containers.DeclarativeContainer):
    core = providers.Container(Core)
    services = providers.Container(Services, core=core)
    handlers = providers.Container(Handlers, services=services)
