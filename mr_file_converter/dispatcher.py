from dependency_injector.wiring import Provide, inject
from telegram.ext import CommandHandler
from telegram.ext.dispatcher import Dispatcher

from mr_file_converter.command.command_service import CommandService
from mr_file_converter.containers import Application
from mr_file_converter.downloader.youtube_downloader_handler import \
    YoutubeDownloaderHandlers
from mr_file_converter.file.file_handler import FileHandlers


@inject
def setup_dispatcher(
    dispatcher: Dispatcher,
    command_service: CommandService = Provide[
        Application.services.command
    ],
    youtube_downloader_handlers: YoutubeDownloaderHandlers = Provide[
        Application.handlers.youtube_downloader
    ],
    file_handlers: FileHandlers = Provide[
        Application.handlers.file
    ]
):
    dispatcher.add_handler(CommandHandler(
        command='help', callback=command_service.help))
    dispatcher.add_handler(CommandHandler(
        command='start', callback=command_service.start))
    dispatcher.add_handler(youtube_downloader_handlers.conversation_handlers())
    dispatcher.add_handler(file_handlers.conversation_handlers())
    dispatcher.add_error_handler(
        callback=command_service.error_handler, run_async=True)
