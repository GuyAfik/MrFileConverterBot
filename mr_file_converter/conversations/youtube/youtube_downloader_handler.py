from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler)

from mr_file_converter.conversations.base_handler import \
    BaseConversationHandler
from mr_file_converter.conversations.youtube.youtube_downloader_conversation import \
    YoutubeDownloaderConversation
from mr_file_converter.services.command.command_service import CommandService


class YoutubeDownloaderHandlers(BaseConversationHandler):

    def __init__(
        self,
        youtube_downloader_conversation: YoutubeDownloaderConversation,
        command_service: CommandService
    ):
        super().__init__(command_service)
        self.youtube_downloader_conversation = youtube_downloader_conversation

    def conversation_handlers(self) -> ConversationHandler:
        return ConversationHandler(
            entry_points=[
                CommandHandler(
                    'youtube',
                    self.youtube_downloader_conversation.ask_youtube_url
                )
            ],
            states={
                self.youtube_downloader_conversation.check_youtube_url_stage: [
                    MessageHandler(
                        Filters.text, self.youtube_downloader_conversation.check_youtube_url
                    )
                ],
                self.youtube_downloader_conversation.download_stage: [
                    CallbackQueryHandler(
                        callback=self.youtube_downloader_conversation.download_video)
                ]
            },
            fallbacks=self.get_fallbacks(),
            run_async=True,
            allow_reentry=True
        )
