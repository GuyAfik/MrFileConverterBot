import os.path

import pytest
from pytest_mock import MockerFixture
from pytube import YouTube
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from mr_file_converter.command.command_service import CommandService
from mr_file_converter.downloader.errors import (InvalidYouTubeURL,
                                                 YouTubeVideoDownloadError)
from mr_file_converter.downloader.youtube_downloader_service import \
    YoutubeDownloaderService
from mr_file_converter.file.file_service import FileService


@pytest.fixture()
def file_test_data_base_path(base_file_path):
    return f'{base_file_path}/file/test_data'


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
    file_service: FileService,
    telegram_update: Update,
    telegram_context: CallbackContext,
    file_test_data_base_path: str,
    file_name: str,
    file_type: str

):
    file_path = f'{file_test_data_base_path}/{file_name}'

    mocker.patch.object(
        file_service.telegram_service,
        'get_file',
        return_value=file_path
    )

    reply_to_message_mocker = mocker.patch.object(
        file_service.telegram_service,
        'reply_to_message'
    )

    next_stage = file_service.check_file_type(
        telegram_update, telegram_context)

    assert reply_to_message_mocker.called
    assert telegram_context.user_data['source_file_path'] == file_path
    assert telegram_context.user_data['source_file_type'] == file_type
    assert next_stage == file_service.ask_custom_file_name_stage
