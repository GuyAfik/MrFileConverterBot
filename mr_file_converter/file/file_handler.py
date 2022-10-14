from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler)

from mr_file_converter.file.file_service import FileService


class FileHandlers:

    def __init__(self, file_service: FileService):
        self.file_service = file_service

    def conversation_handlers(self) -> ConversationHandler:
        return ConversationHandler(
            entry_points=[
                CommandHandler('convert', self.file_service.start_message)
            ],
            states={
                self.file_service.check_file_type_stage: [
                    MessageHandler(
                        Filters.document, self.file_service.check_file_type
                    )
                ],
                self.file_service.covert_file_stage: [
                    CallbackQueryHandler(
                        callback=self.file_service.convert_file)
                ]
            },
            fallbacks=[
                MessageHandler(
                    filters=Filters.regex('^exit$'), callback=self.file_service.command_service.help
                ),
                CommandHandler(
                    "cancel", callback=self.file_service.command_service.cancel)
            ],
            run_async=True,
            allow_reentry=True
        )
