from telegram import Update
from telegram.ext import CallbackContext

from mr_file_converter.telegram.telegram_service import TelegramService
from magic import from_file


class FileService:
    """
    This service is responsible to manage all the operations related to file conversions.
    """
    def __init__(self, telegram_service: TelegramService):
        self.telegram_service = telegram_service

    def check_file_type(self, update: Update, context: CallbackContext):
        file_path = self.telegram_service.get_file(update, context)
        file_type = from_file(file_path)