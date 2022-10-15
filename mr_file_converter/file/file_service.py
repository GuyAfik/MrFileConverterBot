import logging
from typing import Callable

from magic import from_file
from telegram import Update
from telegram.ext import CallbackContext

from mr_file_converter.command.command_service import CommandService
from mr_file_converter.io.io_service import IOService
from mr_file_converter.json.json_service import JsonService
from mr_file_converter.telegram.telegram_service import TelegramService
from mr_file_converter.yaml.yaml_service import YamlService

logger = logging.getLogger(__name__)


class FileService:
    """
    This service is responsible to manage all the operations related to file conversions.
    """
    (
        check_file_type_stage,
        ask_custom_file_name_stage,
        convert_file_stage
    ) = range(3)

    supported_file_formats = {'json, yml'}

    equivalent_file_formats = {
        'application/json': ['yml', 'text', 'xml'],
        'application/yml': ['json', 'text', 'xml']
    }

    def __init__(
        self,
        telegram_service: TelegramService,
        io_service: IOService,
        command_service: CommandService,
        json_service: JsonService,
        yaml_service: YamlService
    ):
        self.telegram_service = telegram_service
        self.io_service = io_service
        self.command_service = command_service
        self.json_service = json_service
        self.yaml_service = yaml_service

    def start_message(self, update: Update, context: CallbackContext):
        self.telegram_service.send_message(
            update=update, text='Please add here a file you would like to convert.')
        return self.check_file_type_stage

    def get_file_type(self, update: Update, context: CallbackContext) -> str | None:
        file_path = self.telegram_service.get_file(update, context)
        context.user_data['source_file_path'] = file_path
        file_type = from_file(file_path, mime=True)

        if file_type in self.equivalent_file_formats:
            return file_type

        if file_type == 'text/plain' and (
            file_path.endswith('yml') or  # type: ignore
            file_path.endswith('yaml')  # type: ignore
        ):
            file_type = 'application/yml'
        else:
            file_type = None
        return file_type

    def check_file_type(self, update: Update, context: CallbackContext) -> int:
        if file_type := self.get_file_type(update, context):
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

        # file type is not supported, cancel conversation
        self.telegram_service.reply_to_message(
            update=update,
            text=f'The file is not supported, supported file formats are:\n{", ".join(self.supported_file_formats)}'
        )
        return self.command_service.cancel(update, context)

    def ask_custom_file_name(self, update: Update, context: CallbackContext) -> int:
        context.user_data['requested_format'] = self.telegram_service.get_message_data(
            update)
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
        except Exception as e:
            error = f'Error occurred when trying to convert the file {source_file_path} ' \
                    f'with format {source_file_type} to requested file format {_requested_format}'
            logger.error(f'{error}, Error is:\n{e}')
            self.telegram_service.send_message(update=update, text=error)
            return self.command_service.cancel(update, context)
        finally:
            self.io_service.remove_file(source_file_path)

    def get_service(self, source_file_type: str, _requested_format: str) -> Callable:  # type: ignore
        if source_file_type == 'application/yml':
            if _requested_format == 'json':
                return self.yaml_service.to_json
            elif _requested_format == 'text':
                return self.yaml_service.to_text
            elif _requested_format == 'xml':
                return self.yaml_service.to_xml
        elif source_file_type == 'application/json':
            if _requested_format == 'yml':
                return self.json_service.to_yml
            elif _requested_format == 'text':
                return self.json_service.to_text
            elif _requested_format == 'xml':
                return self.json_service.to_xml
