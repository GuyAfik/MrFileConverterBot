import logging
import ssl
from typing import Callable
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

    (
        check_url_validity_stage,
        ask_file_name_stage,
        convert_url_stage,
        convert_additional_url_stage
    ) = range(4)

    supported_types = {'pdf', 'html'}

    class FileTypes:
        PDF = 'pdf'
        HTML = 'html'

    def __init__(
        self,
        telegram_service: TelegramService,
        url_service: URLService
    ):
        self.telegram_service = telegram_service
        self.url_service = url_service
        self.urlopen = urlopen

    def start_message(self, update: Update, context: CallbackContext):
        self.telegram_service.send_message(
            update=update, text='Please add here a URL you would like to convert into a file')
        return self.check_url_validity_stage

    def check_url_validity(self, update: Update, context: CallbackContext) -> int:
        def ignore_ssl():
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            return ctx

        url = self.telegram_service.get_message_data(update)
        try:
            self.urlopen(url, context=ignore_ssl())
        except Exception as e:
            logger.error(f'Error:\n{e}')
            raise InvalidURL(
                url=url, next_stage=self.check_url_validity_stage, exception=e)

        context.user_data['url'] = url
        self.telegram_service.reply_to_message(
            update,
            text='url can be formatted to the following file formats, please choose one of them',
            reply_markup=self.telegram_service.get_inline_keyboard(
                buttons=list(self.supported_types))
        )
        return self.ask_file_name_stage

    def ask_custom_file_name(self, update: Update, context: CallbackContext) -> int:
        context.user_data['requested_format'] = self.telegram_service.get_message_data(
            update
        )
        self.telegram_service.send_message(
            update=update,
            text='Please enter the file name you want for the converted file'
        )
        return self.convert_url_stage

    def convert_url(self, update: Update, context: CallbackContext) -> int:
        requested_format = context.user_data.get('requested_format')
        url = context.user_data.get('url')
        custom_file_name = self.telegram_service.get_message_data(update)

        try:
            with self.get_service(
                requested_format
            )(url, custom_file_name) as destination_file_path:
                self.telegram_service.send_file(
                    update, document_path=destination_file_path
                )
                return self.ask_convert_additional_url(update)
        except Exception as e:
            logger.error(f'Error:\n{e}')
            raise URLToFileConversionError(
                url=url,
                target_format=requested_format
            )

    def get_service(self, requested_format: str) -> Callable:  # type: ignore
        if requested_format == self.FileTypes.PDF:
            return self.url_service.to_pdf
        elif requested_format == self.FileTypes.HTML:
            return self.url_service.to_html

    def ask_convert_additional_url(self, update: Update) -> int:
        self.telegram_service.send_message(
            update,
            text='Would you like to convert another url into a file?',
            reply_markup=self.telegram_service.get_inline_keyboard(
                buttons=['yes', 'no']
            )
        )
        return self.convert_additional_url_stage

    def convert_additional_url_answer(self, update: Update, context: CallbackContext) -> int:
        answer = self.telegram_service.get_message_data(update)
        if answer == 'yes':
            return self.start_message(update, context)
        self.telegram_service.edit_message(
            update, text='Thank you! Run /start or /help to view available commands')
        return ConversationHandler.END
