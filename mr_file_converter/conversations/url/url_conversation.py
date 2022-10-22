import logging
from typing import Callable
from urllib.error import URLError
from urllib.request import urlopen

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from mr_file_converter.conversations.url.errors import (
    InvalidURL, URLToFileConversionError)
from mr_file_converter.services.telegram.telegram_service import \
    TelegramService
from mr_file_converter.services.url.url_service import URLService

logger = logging.getLogger(__name__)


class URLConversation:

    check_url_validity_stage, convert_url_stage = range(2)

    supported_types = {'pdf'}

    class FileTypes:
        PDF = 'pdf'

    def __init__(
        self,
        telegram_service: TelegramService,
        url_service: URLService
    ):
        self.telegram_service = telegram_service
        self.url_service = url_service

    def start_message(self, update: Update, context: CallbackContext):
        self.telegram_service.send_message(
            update=update, text='Please add here a URL you would like to convert into a file')
        return self.check_url_validity_stage

    def check_url_validity(self, update: Update, context: CallbackContext):
        url = self.telegram_service.get_message_data(update)
        try:
            if urlopen(url).getcode() != 200:
                raise InvalidURL(
                    url=url, next_stage=self.check_url_validity_stage)
        except (URLError, ValueError) as e:
            logger.error(f'Error:\n{e}')
            raise InvalidURL(url=url, next_stage=self.check_url_validity_stage)

        context.user_data['url'] = url
        self.telegram_service.reply_to_message(
            update,
            text='url can be formatted to the following file formats, please choose one of them',
            reply_markup=self.telegram_service.get_inline_keyboard(
                buttons=list(self.supported_types))
        )
        return self.convert_url_stage

    def convert_url(self, update: Update, context: CallbackContext):
        requested_format = self.telegram_service.get_message_data(update)
        url = context.user_data.get('url')

        # custom_file_name = self.telegram_service.get_message_data(update)

        try:
            with self.get_service(
                requested_format
            )(url, 'bla') as destination_file_path:
                self.telegram_service.send_file(
                    update, document_path=destination_file_path
                )
                return ConversationHandler.END
        except Exception as e:
            logger.error(f'Error:\n{e}')
            raise URLToFileConversionError(
                url=url,
                target_format=requested_format
            )

    def get_service(self, requested_format: str) -> Callable:  # type: ignore
        if requested_format == self.FileTypes.PDF:
            return self.url_service.to_pdf
