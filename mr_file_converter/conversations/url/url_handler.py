from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler)

from mr_file_converter.conversations.url.url_conversation import \
    URLConversation
from mr_file_converter.services.command.command_service import CommandService


class URLHandlers:

    def __init__(self, url_conversation: URLConversation, command_service: CommandService):
        self.url_conversation = url_conversation
        self.command_service = command_service

    def conversation_handlers(self) -> ConversationHandler:
        return ConversationHandler(
            entry_points=[
                CommandHandler('url', self.url_conversation.start_message)
            ],
            states={
                self.url_conversation.check_url_validity_stage: [
                    MessageHandler(
                        Filters.text, self.url_conversation.check_url_validity
                    )
                ],
                self.url_conversation.convert_url_stage: [
                    CallbackQueryHandler(
                        callback=self.url_conversation.convert_url
                    )
                ],
            },
            fallbacks=[
                MessageHandler(
                    filters=Filters.regex('^exit$'), callback=self.command_service.cancel
                ),
                CommandHandler(
                    "cancel", callback=self.command_service.cancel)
            ],
            run_async=True,
            allow_reentry=True
        )
