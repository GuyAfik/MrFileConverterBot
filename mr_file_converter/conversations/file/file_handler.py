from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler)

from mr_file_converter.conversations.file.file_conversation import \
    FileConversation
from mr_file_converter.services.command.command_service import CommandService


class FileHandlers:

    def __init__(self, file_conversation: FileConversation, command_service: CommandService):
        self.file_conversation = file_conversation
        self.command_service = command_service

    def conversation_handlers(self) -> ConversationHandler:
        return ConversationHandler(
            entry_points=[
                CommandHandler('file', self.file_conversation.start_message)
            ],
            states={
                self.file_conversation.check_file_type_stage: [
                    MessageHandler(
                        Filters.document, self.file_conversation.check_file_type
                    )
                ],
                self.file_conversation.ask_custom_file_name_stage: [
                    CallbackQueryHandler(
                        callback=self.file_conversation.ask_custom_file_name
                    )
                ],
                self.file_conversation.convert_file_stage: [
                    MessageHandler(
                        Filters.text, self.file_conversation.convert_file
                    )
                ],
                self.file_conversation.convert_additional_file_answer_stage: [
                    CallbackQueryHandler(
                        callback=self.file_conversation.convert_additional_file_answer
                    )
                ]
            },
            fallbacks=[
                MessageHandler(
                    filters=Filters.regex('^exit$'), callback=self.command_service.cancel
                ),
                CommandHandler(
                    "cancel", callback=self.command_service.cancel
                )
            ],
            run_async=True,
            allow_reentry=True
        )
