import inspect
import logging
import ssl
from typing import Callable
from urllib.request import urlopen

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from mr_file_converter.services.telegram.telegram_service import \
    TelegramService
from mr_file_converter.services.url.errors import (InvalidURL,
                                                   URLToFileConversionError)
from mr_file_converter.services.url.url_service import URLService

logger = logging.getLogger(__name__)


class URLConversation:

    (
        check_url_validity_stage,
        ask_file_name_stage,
        convert_url_stage,
        convert_additional_url_stage
    ) = range(4)

    class FileTypes:
        PDF = 'pdf'
        HTML = 'html'
        PNG = 'png'
        JPG = 'jpg'

        @classmethod
        def supported_file_types(cls) -> list:
            return [
                member[1] for member in inspect.getmembers(cls)
                if not member[0].startswith('_') and not inspect.ismethod(member[1])
            ]

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
            update=update, text='Please add here a URL you would like to convert into a file'
        )
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
            raise InvalidURL(
                url=url, next_stage=self.check_url_validity_stage, exception=e
            )

        context.user_data['url'] = url
        self.telegram_service.reply_to_message(
            update,
            text='url can be formatted to the following file formats, please choose one of them',
            reply_markup=self.telegram_service.get_inline_keyboard(
                buttons=self.FileTypes.supported_file_types()
            )
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
                    update,
                    document_path=destination_file_path,
                    file_name=f'{custom_file_name}.{requested_format}'
                )
                return self.ask_convert_additional_url(update)
        except Exception as e:
            raise URLToFileConversionError(
                url=url,
                target_format=requested_format,
                original_exception=e
            )

    def get_service(self, requested_format: str) -> Callable:
        if requested_format not in self.FileTypes.supported_file_types():
            raise ValueError(
                f'the requested format {requested_format} is not supported'
            )

        format_to_service_func = {
            self.FileTypes.PDF: self.url_service.to_pdf,
            self.FileTypes.HTML: self.url_service.to_html,
            self.FileTypes.PNG: self.url_service.to_png,
            self.FileTypes.JPG: self.url_service.to_jpg
        }

        return format_to_service_func[requested_format]

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
            update, text='Thank you! Run /start or /help to view available commands'
        )
        return ConversationHandler.END
