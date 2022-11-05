import logging

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from mr_file_converter.base_error import FileConverterException
from mr_file_converter.services.io.io_service import IOService
from mr_file_converter.services.telegram.telegram_service import \
    TelegramService

logger = logging.getLogger(__name__)


class CommandService:
    """
    This service provides the interface for the basic commands that this bot supports such as start, cancel, help
    """

    def __init__(self, telegram_service: TelegramService, io_service: IOService):
        self.telegram_service = telegram_service
        self.io_service = io_service

    def help(self, update: Update, context: CallbackContext):
        first_name, last_name = self.telegram_service.get_user_first_and_last_name(
            update
        )
        self.telegram_service.send_message(
            update=update,
            text=f'Hello {first_name} {last_name}, This bot supports the following commands:\n\n'
                 f'1) /file - convert between file types:\n\n'
                 f'  a) json -> yml, text, xml, yml\n'
                 f'  b) yml -> json, text, xml\n'
                 f'  c) xml -> json, yml\n'
                 f'  d) html -> pdf, png, jpg, text\n'
                 f'  e) pdf -> docx, text\n'
                 f'  f) png -> pdf\n\n'
                 f'2) /url - convert URL into files, supported formats: [pdf, png, jpg, html]\n\n'
                 f'3) /youtube - convert youtube video to mp3/mp4'
        )

    def cancel(self, update: Update, context: CallbackContext, next_stage: int = ConversationHandler.END) -> int:
        if source_file_path := context.user_data.get('source_file_path'):
            self.io_service.remove_file(source_file_path)
        if next_stage == ConversationHandler.END:
            self.help(update, context)
        context.user_data.clear()
        return next_stage

    def error_handler(self, update: Update, context: CallbackContext) -> int:
        error = context.error
        should_send_message = True

        logger.error(f'{type(error)=}, {error=}')

        if isinstance(error, FileConverterException):
            if original_exception := error.original_exception:
                logger.error(f'Original Error: {original_exception}')
            next_stage = error.next_stage
            if error.should_reply_to_message_id:
                should_send_message = False
                self.telegram_service.reply_to_message(update, text=f'{error}')
        else:
            next_stage = ConversationHandler.END

        if should_send_message:
            self.telegram_service.send_message(
                update,
                text=f'{error}'
            )

        return self.cancel(update, context, next_stage=next_stage)
