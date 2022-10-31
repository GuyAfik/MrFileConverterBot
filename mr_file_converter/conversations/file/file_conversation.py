import logging
from typing import Callable

from magic import from_file
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from mr_file_converter.conversations.file.errors import (FileConversionError,
                                                         FileTypeNotSupported)
from mr_file_converter.services.html.html_service import HTMLService
from mr_file_converter.services.io.io_service import IOService
from mr_file_converter.services.json.json_service import JsonService
from mr_file_converter.services.pdf.pdf_service import PdfService
from mr_file_converter.services.photo.photo_service import PhotoService
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
        DOCX = 'docx'
        PHOTO = 'photo'  # any photo file type such as photo,jpg

        @classmethod
        def equivalent_file_formats(cls) -> dict:
            return {
                cls.JSON: [cls.YML, cls.TEXT, cls.XML],
                cls.YML: [cls.JSON, cls.TEXT, cls.XML],
                cls.XML: [cls.JSON, cls.YML],
                cls.HTML: [cls.PDF, cls.PNG, cls.JPG, cls.TEXT],
                cls.PDF: [cls.DOCX, cls.TEXT],
                cls.PHOTO: [cls.PDF, cls.TEXT]
            }
    (
        check_file_type_stage,
        ask_custom_file_name_stage,
        convert_file_stage,
        convert_additional_file_answer_stage
    ) = range(4)

    def __init__(
        self,
        telegram_service: TelegramService,
        io_service: IOService,
        json_service: JsonService,
        yaml_service: YamlService,
        xml_service: XMLService,
        html_service: HTMLService,
        pdf_service: PdfService,
        photo_service: PhotoService
    ):
        self.telegram_service = telegram_service
        self.io_service = io_service
        self.json_service = json_service
        self.yaml_service = yaml_service
        self.xml_service = xml_service
        self.html_service = html_service
        self.pdf_service = pdf_service
        self.photo_service = photo_service

    def start_message(self, update: Update, context: CallbackContext):
        self.telegram_service.send_message(
            update=update, text='Please add here a file you would like to convert.')
        return self.check_file_type_stage

    def get_file_type(self, update: Update, context: CallbackContext) -> str:
        file_path = self.telegram_service.get_file(update)
        context.user_data['source_file_path'] = file_path
        file_type = from_file(file_path, mime=True)
        print(file_type)
        print(file_path)
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
        elif file_type == 'application/pdf':
            file_type = self.FileTypes.PDF
        elif 'image' in file_type:
            file_type = self.FileTypes.PHOTO
        return file_type

    def check_file_type(self, update: Update, context: CallbackContext) -> int:
        file_type = self.get_file_type(update, context)
        if equivalent_types := self.FileTypes.equivalent_file_formats().get(file_type):
            context.user_data['source_file_type'] = file_type
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
                    update,
                    document_path=destination_file_path,
                    file_name=f'{custom_file_name}.{_requested_format}'
                )
                self.io_service.remove_file(source_file_path)
                return self.ask_convert_additional_file(update)
        except Exception as e:
            raise FileConversionError(
                source_format=source_file_type,
                target_format=_requested_format,
                original_exception=e
            )

    def get_service(self, source_file_type: str, _requested_format: str) -> Callable:

        format_to_service_func = {
            self.FileTypes.YML: {
                self.FileTypes.JSON: self.yaml_service.to_json,
                self.FileTypes.TEXT: self.yaml_service.to_text,
                self.FileTypes.XML: self.yaml_service.to_xml
            },
            self.FileTypes.JSON: {
                self.FileTypes.YML: self.json_service.to_yml,
                self.FileTypes.TEXT: self.json_service.to_text,
                self.FileTypes.XML: self.json_service.to_xml
            },
            self.FileTypes.XML: {
                self.FileTypes.YML: self.xml_service.to_yml,
                self.FileTypes.JSON: self.xml_service.to_json
            },
            self.FileTypes.HTML: {
                self.FileTypes.PDF: self.html_service.to_pdf,
                self.FileTypes.PNG: self.html_service.to_png,
                self.FileTypes.JPG: self.html_service.to_jpg,
                self.FileTypes.TEXT: self.html_service.to_text
            },
            self.FileTypes.PDF: {
                self.FileTypes.DOCX: self.pdf_service.to_docx,
                self.FileTypes.TEXT: self.pdf_service.to_txt
            },
            self.FileTypes.PHOTO: {
                self.FileTypes.PDF: self.photo_service.to_pdf,
                self.FileTypes.TEXT: self.photo_service.to_text
            }
        }

        return format_to_service_func[source_file_type][_requested_format]

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
