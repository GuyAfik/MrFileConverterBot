from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler)

from mr_file_converter.downloader.youtube_downloader_service import \
    YoutubeDownloaderService


class YoutubeDownloaderHandlers:

    def __init__(self, youtube_downloader_service: YoutubeDownloaderService):
        self.youtube_downloader_service = youtube_downloader_service

    def conversation_handlers(self) -> ConversationHandler:
        return ConversationHandler(
            entry_points=[
                CommandHandler('get_youtube_video',
                               self.youtube_downloader_service.ask_youtube_url)
            ],
            states={
                self.youtube_downloader_service.check_youtube_url_stage: [
                    MessageHandler(
                        Filters.text, self.youtube_downloader_service.check_youtube_url
                    )
                ],
                self.youtube_downloader_service.download_stage: [
                    CallbackQueryHandler(
                        callback=self.youtube_downloader_service.download_video)
                ]
            },
            fallbacks=[
                MessageHandler(
                    filters=Filters.regex('^exit$'), callback=self.youtube_downloader_service.command_service.help
                ),
                CommandHandler(
                    "cancel", callback=self.youtube_downloader_service.command_service.cancel)
            ],
            run_async=True,
            allow_reentry=True
        )
