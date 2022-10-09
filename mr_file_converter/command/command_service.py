from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from mr_file_converter.telegram.telegram_service import TelegramService


class CommandService:
    """
    This service provides the interface for the basic commands that this bot supports such as start, cancel, help
    """
    def __init__(self, telegram_service: TelegramService):
        self.telegram_service = telegram_service

    def start(self, update: Update, context: CallbackContext):
        first_name, last_name = self.telegram_service.get_user_first_and_last_name(update)
        self.telegram_service.send_message(
            update=update, text=f'Welcome {first_name} {last_name}, I am '
                                f'available commands:\n/get_youtube_video: Get youtube video in mp3/mp4 format.'
        )

    def help(self, update: Update, context: CallbackContext):
        self.telegram_service.send_message(
            update=update, text="this is just a stub string at the moment."
        )

    def cancel(self, update: Update, context: CallbackContext):
        self.help(update, context)
        return ConversationHandler.END
