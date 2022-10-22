import pytest
from pytest_mock import MockerFixture
from telegram import Update
from telegram.ext import CallbackContext

from mr_file_converter.conversations.file.errors import FileTypeNotSupported
from mr_file_converter.conversations.file.file_conversation import \
    FileConversation


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
