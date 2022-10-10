from magic import from_file
from telegram import Update
from telegram.ext import CallbackContext

from mr_file_converter.json.json_service import JsonService
from mr_file_converter.telegram.telegram_service import TelegramService
from mr_file_converter.yaml.yaml_service import YamlService


class FileService:
    """
    This service is responsible to manage all the operations related to file conversions.
    """

    def __init__(self, telegram_service: TelegramService, json_service: JsonService, yaml_service: YamlService):
        self.telegram_service = telegram_service
        self.json_service = json_service
        self.yaml_service = yaml_service

    def check_file_type(self, update: Update, context: CallbackContext):
        file_path = self.telegram_service.get_file(update, context)
        file_type = from_file(file_path)
