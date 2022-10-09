from dependency_injector.wiring import Provide, inject
from telegram.ext.dispatcher import Dispatcher

from mr_file_converter.containers import Application
from mr_file_converter.downloader.youtube_downloader_handler import \
    YoutubeDownloaderHandlers


@inject
def setup_dispatcher(
    dispatcher: Dispatcher,
    youtube_downloader_handles: YoutubeDownloaderHandlers = Provide[
        Application.handlers.youtube_downloader
    ]
):
    dispatcher.add_handler(youtube_downloader_handles.conversation_handlers())
