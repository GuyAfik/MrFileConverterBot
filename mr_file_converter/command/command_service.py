from telegram import Message, Update
from telegram.ext import CallbackContext, ConversationHandler

from mr_file_converter.base_error import FileConverterException
from mr_file_converter.io.io_service import IOService
from mr_file_converter.telegram.telegram_service import TelegramService


class CommandService:
    """
    This service provides the interface for the basic commands that this bot supports such as start, cancel, help
    """

    def __init__(self, telegram_service: TelegramService, io_service: IOService):
        self.telegram_service = telegram_service
        self.io_service = io_service

    def start(self, update: Update, context: CallbackContext):
        first_name, last_name = self.telegram_service.get_user_first_and_last_name(
            update)
        self.telegram_service.send_message(
            update=update, text=f'Welcome {first_name} {last_name}, I am MrFileConverterBot, '
                                f'available commands:\n/get_youtube_video: Get youtube video in mp3/mp4 format.'
        )

    def help(self, update: Update, context: CallbackContext):
        self.telegram_service.send_message(
            update=update, text="Available commands: get_youtube_video, convert, start"
        )

    def cancel(self, update: Update, context: CallbackContext, next_stage: int = ConversationHandler.END) -> int:
        if source_file_path := context.user_data.get('source_file_path'):
            self.io_service.remove_file(source_file_path)
        if next_stage == ConversationHandler.END:
            self.help(update, context)
        return next_stage

    def error_handler(self, update: Update, context: CallbackContext) -> int:
        error = context.error

        if hasattr(error, 'next_stage') and error.next_stage >= 0:
            next_stage = error.next_stage
        else:
            next_stage = ConversationHandler.END

        if hasattr(error, 'should_reply_to_message_id') and error.should_reply_to_message_id:
            self.telegram_service.reply_to_message(update, text=f'{error}')
        else:
            self.telegram_service.send_message(
                update=update,
                text=f'{error}'
            )

        return self.cancel(update, context, next_stage=next_stage)
