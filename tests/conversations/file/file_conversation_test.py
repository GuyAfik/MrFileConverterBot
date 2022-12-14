import os.path

import pytest
from pytest_mock import MockerFixture
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from mr_file_converter.conversations.file.errors import FileTypeNotSupported
from mr_file_converter.conversations.file.file_conversation import \
    FileConversation
from mr_file_converter.services.html.html_service import HTMLService
from mr_file_converter.services.io.io_service import IOService
from mr_file_converter.services.json.json_service import JsonService
from mr_file_converter.services.pdf.pdf_service import PdfService
from mr_file_converter.services.photo.photo_service import PhotoService
from mr_file_converter.services.telegram.telegram_service import \
    TelegramService
from mr_file_converter.services.xml.xml_service import XMLService
from mr_file_converter.services.yaml.yaml_service import YamlService


@pytest.fixture()
def file_conversation(
    telegram_service: TelegramService,
    io_service: IOService,
    json_service: JsonService,
    yml_service: YamlService,
    xml_service: XMLService,
    html_service: HTMLService,
    pdf_service: PdfService,
    photo_service: PhotoService
) -> FileConversation:
    return FileConversation(
        telegram_service=telegram_service,
        io_service=io_service,
        json_service=json_service,
        yaml_service=yml_service,
        xml_service=xml_service,
        html_service=html_service,
        pdf_service=pdf_service,
        photo_service=photo_service
    )


@pytest.fixture()
def file_test_data_base_path(base_file_path) -> str:
    return f'{base_file_path}/conversations/file/test_data'


@pytest.mark.parametrize(
    'file_name, file_type',
    [
        ('test.json', 'json'),
        ('test.html', 'html'),
        ('test.yml', 'yml'),
        ('test.xml', 'xml')
    ]
)
def test_check_file_supported_file_type(
    mocker: MockerFixture,
    file_conversation: FileConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
    file_test_data_base_path: str,
    file_name: str,
    file_type: str
):
    """
    Given:
     - supported files

    When:
     - running the 'check_file_type' method

    Then:
     - make sure there is a reply message saying the file type is supported
     - make sure the file path / type is saved in the context
     - make sure the next stage is the 'ask_custom_file_name_stage'
    """
    file_path = f'{file_test_data_base_path}/{file_name}'

    mocker.patch.object(
        file_conversation.telegram_service,
        'get_file',
        return_value=file_path
    )

    reply_to_message_mocker = mocker.patch.object(
        file_conversation.telegram_service,
        'reply_to_message'
    )

    next_stage = file_conversation.check_file_type(
        telegram_update, telegram_context
    )

    assert reply_to_message_mocker.called
    assert telegram_context.user_data['source_file_path'] == file_path
    assert telegram_context.user_data['source_file_type'] == file_type
    assert next_stage == file_conversation.ask_custom_file_name_stage


@pytest.mark.parametrize(
    'file_name',
    [
        'test.dxf',
        'test.eps'
    ]
)
def test_check_file_type_unsupported_file(
    mocker: MockerFixture,
    file_conversation: FileConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
    file_test_data_base_path: str,
    file_name: str,
):
    """
    Given:
     - unsupported files

    When:
     - running the 'check_file_type' method

    Then:
     - make sure the 'FileTypeNotSupported' exception is raised
    """
    mocker.patch.object(
        file_conversation.telegram_service,
        'get_file',
        return_value=f'{file_test_data_base_path}/{file_name}'
    )

    with pytest.raises(FileTypeNotSupported):
        file_conversation.check_file_type(
            telegram_update, telegram_context
        )


def test_convert_additional_file_yes_option(
    mocker: MockerFixture,
    file_conversation: FileConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
):
    """
    Given:
     - 'yes' marked option to get additional file

    When:
     - running 'convert_additional_file_answer' method

    Then:
     - make sure the next stage is the 'check_file_type_stage' (first stage in the conversation)
    """
    mocker.patch.object(
        file_conversation.telegram_service,
        'get_message_data',
        return_value='yes'
    )
    send_message_mocker = mocker.patch.object(
        file_conversation.telegram_service, 'send_message'
    )

    next_stage = file_conversation.convert_additional_file_answer(
        telegram_update, telegram_context
    )

    assert send_message_mocker.called
    assert next_stage == file_conversation.check_file_type_stage


def test_convert_additional_file_no_option(
    mocker: MockerFixture,
    file_conversation: FileConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
):
    """
    Given:
     - 'no' marked option to get additional file

    When:
     - running 'convert_additional_file_answer' method

    Then:
     - make sure the next stage is the 'ConversationHandler.END'
    """
    mocker.patch.object(
        file_conversation.telegram_service,
        'get_message_data',
        return_value='no'
    )
    edit_message_mocker = mocker.patch.object(
        file_conversation.telegram_service, 'edit_message'
    )

    next_stage = file_conversation.convert_additional_file_answer(
        telegram_update, telegram_context
    )

    assert edit_message_mocker.called
    assert next_stage == ConversationHandler.END


@pytest.mark.parametrize(
    'file_name, file_type, requested_format',
    [
        ('test.json', 'json', 'yml'),
        ('test.json', 'json', 'xml'),
        ('test.json', 'json', 'text'),
        ('test.yml', 'yml', 'json'),
        ('test.yml', 'yml', 'xml'),
        ('test.yml', 'yml', 'text'),
        ('test.xml', 'xml', 'json'),
        ('test.xml', 'xml', 'yml'),
        ('test.pdf', 'pdf', 'docx'),
        ('test.pdf', 'pdf', 'text'),
        ('test.html', 'html', 'text'),
        ('test.html', 'html', 'jpg'),
        ('test.html', 'html', 'png'),
        ('test.html', 'html', 'pdf'),
        ('test.jpg', 'photo', 'text'),
        ('test.png', 'photo', 'pdf'),
    ]
)
def test_convert_file(
    mocker: MockerFixture,
    file_conversation: FileConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
    file_test_data_base_path: str,
    file_name: str,
    file_type: str,
    requested_format: str
):
    """
    Given:
     - Case 1: json file to yml file
     - Case 2: json file to xml file
     - Case 3: json file to text file
     - Case 4: yml file to json file
     - Case 5: yml file to xml file
     - Case 6: yml file to text file
     - Case 7: xml file to json file
     - Case 8: xml file to yml file
     - Case 9: pdf file to docx file
     - Case 10: pdf file to text file
     - Case 11: html file to text file
     - Case 12: html file to jpg file
     - Case 13: html file to png file
     - Case 14: html file to pdf file
     - Case 15: jpg file to text file
     - Case 16: png file to pdf

    When:
     - running 'convert file' method

    Then:
     - make sure file was sent with the correct name and suffix that user requested
     - make sure the file conversion succeeds
     - make sure the next stage is the 'convert_additional_file_answer_stage'
    """
    telegram_context.user_data['requested_format'] = requested_format
    telegram_context.user_data['source_file_type'] = file_type
    telegram_context.user_data['source_file_path'] = f'{file_test_data_base_path}/{file_name}'

    send_file_mocker = mocker.patch.object(
        file_conversation.telegram_service, 'send_file')
    mocker.patch.object(
        file_conversation.telegram_service,
        'get_message_data',
        return_value='file_name'
    )
    next_stage = file_conversation.convert_file(
        telegram_update, telegram_context, should_delete_source_file=False
    )
    assert send_file_mocker.called
    file_name = send_file_mocker.call_args.kwargs['file_name']
    assert file_name == f'file_name.{requested_format}'
    assert next_stage == file_conversation.convert_additional_file_answer_stage
