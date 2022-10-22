import logging
from typing import Callable

from magic import from_file
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from mr_file_converter.conversations.file.errors import (FileConversionError,
                                                         FileTypeNotSupported)
from mr_file_converter.services.command.command_service import CommandService
from mr_file_converter.services.html.html_service import HTMLService
from mr_file_converter.services.io.io_service import IOService
from mr_file_converter.services.json.json_service import JsonService
from mr_file_converter.services.telegram.telegram_service import \
    TelegramService
from mr_file_converter.services.xml.xml_service import XMLService
from mr_file_converter.services.yaml.yaml_service import YamlService

logger = logging.getLogger(__name__)


class FileConversation:
    """
    This service is responsible to manage all the operations related to file conversions.
    """
    class FileTypes:
        YML = 'yml'
        JSON = 'json'
        XML = 'xml'
        TEXT = 'text'
        HTML = 'html'
        PDF = 'pdf'
        PNG = 'png'
        JPG = 'jpg'

    (
        check_file_type_stage,
        ask_custom_file_name_stage,
        convert_file_stage,
        convert_additional_file_answer_stage
    ) = range(4)

    equivalent_file_formats = {
        FileTypes.JSON: [FileTypes.YML, FileTypes.TEXT, FileTypes.XML],
        FileTypes.YML: [FileTypes.JSON, FileTypes.TEXT, FileTypes.XML],
        FileTypes.XML: [FileTypes.JSON, FileTypes.YML],
        FileTypes.HTML: [FileTypes.PDF, FileTypes.PNG, FileTypes.JPG]
    }

    def __init__(
        self,
        telegram_service: TelegramService,
        io_service: IOService,
        json_service: JsonService,
        yaml_service: YamlService,
        xml_service: XMLService,
        html_service: HTMLService
    ):
        self.telegram_service = telegram_service
        self.io_service = io_service
        self.json_service = json_service
        self.yaml_service = yaml_service
        self.xml_service = xml_service
        self.html_service = html_service

    def start_message(self, update: Update, context: CallbackContext):
        self.telegram_service.send_message(
            update=update, text='Please add here a file you would like to convert.')
        return self.check_file_type_stage

    def get_file_type(self, update: Update, context: CallbackContext) -> str:
        file_path = self.telegram_service.get_file(update, context)
        context.user_data['source_file_path'] = file_path
        file_type = from_file(file_path, mime=True)
        print(file_type)
        logger.debug(f'The type of the file {file_path} is {file_type}')

        if file_type == 'text/plain' and (
            file_path.endswith('yml') or  # type: ignore
            file_path.endswith('yaml')  # type: ignore
        ):
            file_type = self.FileTypes.YML
        elif file_type == 'text/xml' and (
            file_path.endswith('xml')  # type: ignore
        ):
            file_type = self.FileTypes.XML
        elif file_type == 'application/json':
            file_type = self.FileTypes.JSON
        elif file_type == 'text/html':
            file_type = self.FileTypes.HTML
        return file_type

    def check_file_type(self, update: Update, context: CallbackContext) -> int:
        file_type = self.get_file_type(update, context)
        if file_type in self.equivalent_file_formats:
            context.user_data['source_file_type'] = file_type
            equivalent_types = self.equivalent_file_formats.get(file_type, [])
            self.telegram_service.reply_to_message(
                update=update,
                text=f'The type of the file is {file_type}, It can be converted to the following types, '
                     f'please choose one of the types to convert into.',
                reply_markup=self.telegram_service.get_inline_keyboard(
                    buttons=equivalent_types
                )
            )
            return self.ask_custom_file_name_stage

        raise FileTypeNotSupported(_file_type=file_type)

    def ask_custom_file_name(self, update: Update, context: CallbackContext) -> int:
        context.user_data['requested_format'] = self.telegram_service.get_message_data(
            update
        )
        self.telegram_service.send_message(
            update=update,
            text='Please enter the file name you want for the converted file'
        )
        return self.convert_file_stage

    def convert_file(self, update: Update, context: CallbackContext):
        _requested_format = context.user_data.get('requested_format')
        source_file_type = context.user_data.get('source_file_type')
        source_file_path = context.user_data.get('source_file_path')
        custom_file_name = self.telegram_service.get_message_data(update)

        try:
            with self.get_service(
                source_file_type, _requested_format
            )(source_file_path, custom_file_name) as destination_file_path:
                self.telegram_service.send_file(
                    update, document_path=destination_file_path
                )
                self.io_service.remove_file(source_file_path)
                return self.ask_convert_additional_file(update)
        except Exception as e:
            logger.error(f'Error:\n{e}')
            raise FileConversionError(
                source_format=source_file_type,
                target_format=_requested_format
            )

    def get_service(self, source_file_type: str, _requested_format: str) -> Callable:  # type: ignore
        if source_file_type == self.FileTypes.YML:
            if _requested_format == self.FileTypes.JSON:
                return self.yaml_service.to_json
            elif _requested_format == self.FileTypes.TEXT:
                return self.yaml_service.to_text
            elif _requested_format == self.FileTypes.XML:
                return self.yaml_service.to_xml
        elif source_file_type == self.FileTypes.JSON:
            if _requested_format == self.FileTypes.YML:
                return self.json_service.to_yml
            elif _requested_format == self.FileTypes.TEXT:
                return self.json_service.to_text
            elif _requested_format == self.FileTypes.XML:
                return self.json_service.to_xml
        elif source_file_type == self.FileTypes.XML:
            if _requested_format == self.FileTypes.YML:
                return self.xml_service.to_yml
            elif _requested_format == self.FileTypes.JSON:
                return self.xml_service.to_json
        elif source_file_type == self.FileTypes.HTML:
            if _requested_format == self.FileTypes.PDF:
                return self.html_service.to_pdf
            if _requested_format == self.FileTypes.PNG:
                return self.html_service.to_png
            if _requested_format == self.FileTypes.JPG:
                return self.html_service.to_jpg

    def ask_convert_additional_file(self, update: Update) -> int:
        self.telegram_service.send_message(
            update,
            text='Would you like to convert another file?',
            reply_markup=self.telegram_service.get_inline_keyboard(
                buttons=['yes', 'no']
            )
        )
        return self.convert_additional_file_answer_stage

    def convert_additional_file_answer(self, update: Update, context: CallbackContext) -> int:
        answer = self.telegram_service.get_message_data(update)
        if answer == 'yes':
            return self.start_message(update, context)
        self.telegram_service.edit_message(
            update, text='Thank you! Run /start or /help to view available commands')
        return ConversationHandler.END
