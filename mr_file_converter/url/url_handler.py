from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler)

from mr_file_converter.command.command_service import CommandService
from mr_file_converter.url.url_service import URLService


class URLHandlers:

    def __init__(self, url_service: URLService, command_service: CommandService):
        self.url_service = url_service
        self.command_service = command_service

    def conversation_handlers(self) -> ConversationHandler:
        return ConversationHandler(
            entry_points=[
                CommandHandler('url', self.url_service.start_message)
            ],
            states={
                self.url_service.check_url_validity_stage: [
                    MessageHandler(
                        Filters.text, self.url_service.check_url_validity
                    )
                ],
                self.url_service.convert_url_stage: [
                    CallbackQueryHandler(
                        callback=self.url_service.convert_url
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
