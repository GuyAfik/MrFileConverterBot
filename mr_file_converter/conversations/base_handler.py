from telegram.ext import MessageHandler, Filters, CommandHandler

from mr_file_converter.services.command.command_service import CommandService


class BaseConversationHandler:

    def __init__(self, command_service: CommandService):
        self.command_service = command_service

    def get_fallbacks(self, regex='^exit$'):
        return [
            MessageHandler(
                filters=Filters.regex(regex),
                callback=self.command_service.cancel
            ),
            CommandHandler(
                "cancel", callback=self.command_service.cancel
            )
        ]
