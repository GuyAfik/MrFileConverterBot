from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler)

from mr_file_converter.conversations.youtube.youtube_downloader_conversation import \
    YoutubeDownloaderConversation


class YoutubeDownloaderHandlers:

    def __init__(self, youtube_downloader_conversation: YoutubeDownloaderConversation):
        self.youtube_downloader_conversation = youtube_downloader_conversation

    def conversation_handlers(self) -> ConversationHandler:
        return ConversationHandler(
            entry_points=[
                CommandHandler('get_youtube_video',
                               self.youtube_downloader_conversation.ask_youtube_url)
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
            fallbacks=[
                MessageHandler(
                    filters=Filters.regex('^exit$'),
                    callback=self.youtube_downloader_conversation.command_service.cancel
                ),
                CommandHandler(
                    "cancel", callback=self.youtube_downloader_conversation.command_service.cancel)
            ],
            run_async=True,
            allow_reentry=True
        )
