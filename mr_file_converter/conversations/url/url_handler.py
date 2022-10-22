from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler)

from mr_file_converter.conversations.base_handler import \
    BaseConversationHandler
from mr_file_converter.conversations.url.url_conversation import \
    URLConversation
from mr_file_converter.services.command.command_service import CommandService


class URLHandlers(BaseConversationHandler):

    def __init__(self, url_conversation: URLConversation, command_service: CommandService):
        super().__init__(command_service)
        self.url_conversation = url_conversation

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
            fallbacks=self.get_fallbacks(),
            run_async=True,
            allow_reentry=True
        )
