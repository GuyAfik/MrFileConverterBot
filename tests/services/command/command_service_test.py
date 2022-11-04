import os.path

import pytest
from pytest_mock import MockerFixture
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from mr_file_converter.conversations.file.errors import (FileConversionError,
                                                         FileTypeNotSupported)
from mr_file_converter.conversations.url.url_conversation import \
    URLConversation
from mr_file_converter.conversations.youtube.youtube_downloader_conversation import \
    YoutubeDownloaderConversation
from mr_file_converter.services.command.command_service import CommandService
from mr_file_converter.services.downloader.errors import (
    InvalidYouTubeURL, YouTubeVideoDownloadError)
from mr_file_converter.services.io.io_service import IOService
from mr_file_converter.services.telegram.telegram_service import \
    TelegramService
from mr_file_converter.services.url.errors import (InvalidURL,
                                                   URLToFileConversionError)


@pytest.fixture()
def command_service(io_service: IOService, telegram_service: TelegramService):
    return CommandService(
        telegram_service=telegram_service, io_service=io_service
    )


class TestErrorHandler:

    def test_error_handler_file_not_supported_exception(
        self,
        mocker: MockerFixture,
        command_service: CommandService,
        telegram_update: Update,
        telegram_context: CallbackContext
    ):
        """
        Given:
         - FileTypeNotSupported exception that was raised.

        When:
         - executing the 'error_handler'

        Then:
         - make sure the next stage is the 'ConversationHandler.END'
         - make sure that there are two messages that were sent, the first is the exception error,
           the second is the help msg.
        """
        send_message_mock = mocker.patch.object(
            command_service.telegram_service, 'send_message'
        )
        telegram_context.error = FileTypeNotSupported(_file_type='test')
        next_stage = command_service.error_handler(
            telegram_update, telegram_context
        )

        assert next_stage == ConversationHandler.END
        # help message should also be called because conversation ended.
        assert len(send_message_mock.call_args_list) == 2
        telegram_err_msg = 'file is of type test and is not supported at the moment'
        assert send_message_mock.call_args_list[0].kwargs['text'] == telegram_err_msg

    def test_error_handler_file_conversion_error_exception(
        self,
        mocker: MockerFixture,
        command_service: CommandService,
        telegram_update: Update,
        telegram_context: CallbackContext
    ):
        """
        Given:
         - FileConversionError exception that was raised.

        When:
         - executing the 'error_handler'

        Then:
         - make sure the next stage is the 'ConversationHandler.END'
         - make sure that there are two messages that were sent, the first is the exception error,
           the second is the help msg.
        """
        send_message_mock = mocker.patch.object(
            command_service.telegram_service, 'send_message'
        )
        telegram_context.error = FileConversionError(
            source_format='json', target_format='yml'
        )
        next_stage = command_service.error_handler(
            telegram_update, telegram_context
        )
        assert next_stage == ConversationHandler.END
        # help message should also be called because conversation ended.
        assert len(send_message_mock.call_args_list) == 2
        telegram_err_msg = 'Error when converting from source format json to target format yml'
        assert send_message_mock.call_args_list[0].kwargs['text'] == telegram_err_msg

    def test_error_handler_invalid_youtube_url_exception(
        self,
        mocker: MockerFixture,
        command_service: CommandService,
        telegram_update: Update,
        telegram_context: CallbackContext
    ):
        """
        Given:
        - InvalidYouTubeURL exception that was raised.

        When:
        - executing the 'error_handler'

        Then:
        - make sure the next stage is the 'YoutubeDownloaderService.check_youtube_url_stage'
        - make sure that the help message is not sent since next stage is not ConversationHandler.END
        - make sure the reply_to_message was sent along with the error exception
       """
        send_message_mock = mocker.patch.object(
            command_service.telegram_service, 'send_message'
        )
        reply_message_mock = mocker.patch.object(
            command_service.telegram_service, 'reply_to_message'
        )
        telegram_context.error = InvalidYouTubeURL(
            url='youtube.test',
            next_stage=YoutubeDownloaderConversation.check_youtube_url_stage
        )
        next_stage = command_service.error_handler(
            telegram_update, telegram_context
        )
        assert next_stage == YoutubeDownloaderConversation.check_youtube_url_stage
        # make sure help message is not sent.
        assert not send_message_mock.called
        telegram_err_msg = 'URL youtube.test is not a valid YouTube video, Please enter again a valid URL'
        assert reply_message_mock.called
        assert reply_message_mock.call_args.kwargs['text'] == telegram_err_msg

    def test_error_handler_youtube_video_download_error(
        self,
        mocker: MockerFixture,
        command_service: CommandService,
        telegram_update: Update,
        telegram_context: CallbackContext
    ):
        """
        Given:
        - YouTubeVideoDownloadError exception that was raised.

        When:
        - executing the 'error_handler'

        Then:
        - make sure the next stage is the 'ConversationHandler.END'
        - make sure that there are two messages that were sent, the first is the exception error,
          the second is the help msg.
       """
        send_message_mock = mocker.patch.object(
            command_service.telegram_service, 'send_message'
        )
        telegram_context.error = YouTubeVideoDownloadError(
            url='youtube_url', _format='mp3'
        )
        next_stage = command_service.error_handler(
            telegram_update, telegram_context
        )
        assert next_stage == ConversationHandler.END
        # help message should also be called because conversation ended.
        assert len(send_message_mock.call_args_list) == 2
        telegram_err_msg = 'Failed to download YouTube video youtube_url as mp3'
        assert send_message_mock.call_args_list[0].kwargs['text'] == telegram_err_msg

    @pytest.mark.parametrize(
        'telegram_err_msg, exception',
        [
            (
                'the url google.com is invalid, please enter a valid url',
                ValueError('invalid url')
            ),
            (
                'Unable to read google.com, please try a different url',
                Exception('unable to establish connection')
            )
        ]
    )
    def test_error_handler_invalid_url(
        self,
        mocker: MockerFixture,
        command_service: CommandService,
        telegram_update: Update,
        telegram_context: CallbackContext,
        telegram_err_msg: str,
        exception: Exception
    ):
        """
        Given:
            Case A:
                - InvalidURL exception that was raised.
                - ValueError as the original exception meaning url is invalid
            Case B:
                - InvalidURL exception that was raised.
                - Exception as the original exception meaning that its wasn't possible to connect to url

        When:
        - executing the 'error_handler'

        Then:
        - make sure the next stage is the 'check_url_validity_stage'
        - make send_message method of telegram service wasn't called
        - make sure reply_message of telegram service was called with the correct message
       """
        reply_to_message_mock = mocker.patch.object(
            command_service.telegram_service, 'reply_to_message'
        )
        send_message_mock = mocker.patch.object(
            command_service.telegram_service, 'send_message'
        )
        telegram_context.error = InvalidURL(
            url='google.com',
            next_stage=URLConversation.check_url_validity_stage,
            exception=exception
        )
        next_stage = command_service.error_handler(
            telegram_update, telegram_context
        )
        assert next_stage == URLConversation.check_url_validity_stage
        assert not send_message_mock.called
        assert reply_to_message_mock.call_args_list[0].kwargs['text'] == telegram_err_msg

    def test_error_handler_url_to_file_conversion_error(
        self,
        mocker: MockerFixture,
        command_service: CommandService,
        telegram_update: Update,
        telegram_context: CallbackContext
    ):
        """
        Given:
        - URLToFileConversionError exception that was raised.

        When:
        - executing the 'error_handler'

        Then:
        - make sure the next stage is the 'ConversationHandler.END'
        - make sure that there are two messages that were sent, the first is the exception error,
          the second is the help msg.
       """
        send_message_mock = mocker.patch.object(
            command_service.telegram_service, 'send_message'
        )
        telegram_context.error = URLToFileConversionError(
            url='https://www.google.com/', target_format='pdf'
        )
        next_stage = command_service.error_handler(
            telegram_update, telegram_context
        )
        assert next_stage == ConversationHandler.END
        # help message should also be called because conversation ended.
        assert len(send_message_mock.call_args_list) == 2
        telegram_err_msg = 'Error when converting URL https://www.google.com/ to target file format pdf'
        assert send_message_mock.call_args_list[0].kwargs['text'] == telegram_err_msg


def test_cancel_delete_source_file_path(
    mocker: MockerFixture,
    command_service: CommandService,
    telegram_update: Update,
    telegram_context: CallbackContext
):
    """
    Given:
     - a trigger to cancel any conversation
     - a source file path that exists in the context
     - next_stage = 'ConversationHandler.END'

    When:
     - executing the cancel method

    Then:
     - make sure the source file gets deleted
     - make sure next stage is the 'ConversationHandler.END' which ends the conversation
     - make sure the help message is called when next_stage == 'ConversationHandler.END'
    """
    file_name = 'test_file'
    telegram_context.user_data['source_file_path'] = open(file_name, 'w').name
    help_mocker = mocker.patch.object(command_service, 'help')
    next_stage = command_service.cancel(telegram_update, telegram_context)

    assert not os.path.exists(file_name)
    assert next_stage == ConversationHandler.END
    assert help_mocker.called
