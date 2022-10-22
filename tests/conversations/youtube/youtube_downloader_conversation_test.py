import os.path

import pytest
from pytest_mock import MockerFixture
from pytube import YouTube
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from mr_file_converter.conversations.youtube.errors import (
    InvalidYouTubeURL, YouTubeVideoDownloadError)
from mr_file_converter.conversations.youtube.youtube_downloader_conversation import \
    YoutubeDownloaderConversation
from mr_file_converter.services.telegram.telegram_service import \
    TelegramService


@pytest.fixture()
def youtube_downloader_conversation(
    telegram_service: TelegramService,
) -> YoutubeDownloaderConversation:
    return YoutubeDownloaderConversation(telegram_service=telegram_service)


def test_check_url_stage_valid_url(
    mocker: MockerFixture,
    youtube_downloader_conversation: YoutubeDownloaderConversation,
    telegram_update: Update,
    telegram_context: CallbackContext
):
    """
    Given:
     - valid youtube URL

    When:
     - executing the 'check_youtube_url' stage

    Then:
     - make sure the YouTube object is saved in context
     - make sure the next stage should be download stage.
     - make sure a message was sent with an inline keyboard was sent with 'mp3' and 'mp4'
    """
    mocker.patch.object(
        youtube_downloader_conversation.telegram_service,
        'get_message_data',
        return_value='https://www.youtube.com/watch?v=xcMRjfT10h0&list=RD7pKrVB5f2W0&index=7'
    )
    send_message_mock = mocker.patch.object(
        youtube_downloader_conversation.telegram_service,
        'send_message'
    )
    next_stage = youtube_downloader_conversation.check_youtube_url(
        update=telegram_update, context=telegram_context
    )
    assert next_stage == youtube_downloader_conversation.download_stage
    assert send_message_mock.called
    assert send_message_mock.call_args.kwargs['reply_markup'].inline_keyboard[0][0].text == 'mp3'
    assert send_message_mock.call_args.kwargs['reply_markup'].inline_keyboard[0][1].text == 'mp4'
    assert 'youtube' in telegram_context.user_data


def test_check_invalid_youtube_url(
    mocker: MockerFixture,
    youtube_downloader_conversation: YoutubeDownloaderConversation,
    telegram_update: Update,
    telegram_context: CallbackContext
):
    """
    Given:
     - invalid youtube URL

    When:
     - executing the 'check_youtube_url' stage

    Then:
     - make sure the InvalidYouTubeURL exception is raised to trigger the error handler.
     - make sure the next stage that is being passed to the exception is the 'check_youtube_url_stage'
     - make sure that the attribute 'should_reply_to_message_id' is set to True.
    """
    mocker.patch.object(
        youtube_downloader_conversation.telegram_service,
        'get_message_data',
        return_value='youtube.blabla'
    )

    with pytest.raises(InvalidYouTubeURL) as excinfo:
        youtube_downloader_conversation.check_youtube_url(
            update=telegram_update, context=telegram_context
        )

    assert excinfo.value.next_stage == youtube_downloader_conversation.check_youtube_url_stage
    assert excinfo.value.should_reply_to_message_id


@pytest.mark.parametrize(
    'invalid_youtube_urls',
    [
        ['a'],
        ['a', 'b'],
        ['a', 'b', 'c']
    ]
)
def test_invalid_youtube_url_flow(
    mocker: MockerFixture,
    youtube_downloader_conversation: YoutubeDownloaderConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
    invalid_youtube_urls
):
    """
    Given:
     - a bunch of invalid YouTube URLs and last one a valid youtube URL.

    When:
     - executing the 'check_youtube_url' stage

    Then:
     - make sure the InvalidYouTubeURL exception is as long as the YouTube URL is invalid.
     - make sure the YouTube object is saved in context only when the YouTube URL is valid
     - make sure the next stage should be download stage when the YouTube URL is valid.
     - make sure a message was sent with an inline keyboard was sent with 'mp3' and 'mp4' when the YouTube URL is valid.
    """
    mocker.patch.object(
        youtube_downloader_conversation.telegram_service,
        'get_message_data',
        side_effect=invalid_youtube_urls +
        ['https://www.youtube.com/watch?v=rn9AQoI7mYU&list=RD7pKrVB5f2W0&index=5']
    )

    for _ in range(len(invalid_youtube_urls)):
        with pytest.raises(InvalidYouTubeURL):
            youtube_downloader_conversation.check_youtube_url(
                update=telegram_update, context=telegram_context
            )

    send_message_mock = mocker.patch.object(
        youtube_downloader_conversation.telegram_service,
        'send_message'
    )
    next_stage = youtube_downloader_conversation.check_youtube_url(
        update=telegram_update, context=telegram_context
    )
    assert next_stage == youtube_downloader_conversation.download_stage
    assert send_message_mock.called
    assert send_message_mock.call_args.kwargs['reply_markup'].inline_keyboard[0][0].text == 'mp3'
    assert send_message_mock.call_args.kwargs['reply_markup'].inline_keyboard[0][1].text == 'mp4'
    assert 'youtube' in telegram_context.user_data


def test_download_video_as_mp3(
    mocker: MockerFixture,
    youtube_downloader_conversation: YoutubeDownloaderConversation,
    telegram_update: Update,
    telegram_context: CallbackContext
):
    """
    Given:
     - mp3 requested format
     - successful YouTube download audio operation

    When:
     - executing the 'download_video' stage

    Then:
     - make sure that the downloaded mp3 file is eventually getting deleted after it has been used.
     - make sure that the next stage is the end of the conversation.
     - make sure that the file was sent as mp3 to telegram api before deletion.
    """
    mocker.patch.object(youtube_downloader_conversation.telegram_service,
                        'get_message_data', return_value='mp3')
    send_audio_mocker = mocker.patch.object(
        youtube_downloader_conversation.telegram_service, 'send_audio')
    mocker.patch.object(
        youtube_downloader_conversation.telegram_service, 'edit_message')
    mocker.patch.object(
        youtube_downloader_conversation.telegram_service, 'get_message_id')
    mocker.patch.object(
        youtube_downloader_conversation.youtube_audio_downloader_cls,
        'download',
        # pytube creates audio files with mp4
        return_value=open('test.mp4', 'w').name
    )
    next_stage = youtube_downloader_conversation.download_video(
        telegram_update, telegram_context)
    assert not os.path.exists('test.mp3')
    assert not os.path.exists('test.mp4')
    assert next_stage == ConversationHandler.END
    assert send_audio_mocker.called
    assert send_audio_mocker.call_args.kwargs['audio_file_path'] == 'test.mp3'


def test_download_mp3_failure(
    mocker: MockerFixture,
    youtube_downloader_conversation: YoutubeDownloaderConversation,
    telegram_update: Update,
    telegram_context: CallbackContext
):
    """
    Given:
     - mp3 requested format
     - download operation to mp3 which failed
     - YouTube object with valid URL

    When:
     - executing the 'download_video' stage

    Then:
     - make sure the YouTubeVideoDownloadError exception is raised.
     - make sure the right error is being raised with the correct URL.
    """
    def throw_exception():
        raise Exception('could not download youtube video as mp3')

    mocker.patch.object(
        youtube_downloader_conversation.telegram_service,
        'get_message_data',
        return_value='mp3'
    )
    mocker.patch.object(
        youtube_downloader_conversation.telegram_service, 'edit_message'
    )

    mocker.patch.object(
        youtube_downloader_conversation.youtube_audio_downloader_cls,
        'download',
        side_effect=throw_exception
    )

    telegram_context.user_data['youtube'] = YouTube(
        'https://www.youtube.com/watch?v=rn9AQoI7mYU&list=RD7pKrVB5f2W0&index=5'
    )

    with pytest.raises(YouTubeVideoDownloadError) as excinfo:
        youtube_downloader_conversation.download_video(
            telegram_update, telegram_context
        )

    assert excinfo.value.args[0] == 'Failed to download YouTube video https://youtube.com/watch?v=rn9AQoI7mYU as mp3'


def test_download_video_as_mp4(
    mocker: MockerFixture,
    youtube_downloader_conversation: YoutubeDownloaderConversation,
    telegram_update: Update,
    telegram_context: CallbackContext
):
    """
    Given:
     - mp4 requested format
     - successful YouTube download video operation

    When:
     - executing the 'download_video' stage

    Then:
     - make sure that the downloaded mp4 file is eventually getting deleted after it has been used.
     - make sure that the next stage is the end of the conversation.
     - make sure that the file was sent as mp4 to telegram api before deletion.
    """
    mocker.patch.object(youtube_downloader_conversation.telegram_service,
                        'get_message_data', return_value='mp4')
    send_video_mocker = mocker.patch.object(
        youtube_downloader_conversation.telegram_service, 'send_video')
    mocker.patch.object(
        youtube_downloader_conversation.telegram_service, 'edit_message')
    mocker.patch.object(
        youtube_downloader_conversation.telegram_service, 'get_message_id')
    mocker.patch.object(
        youtube_downloader_conversation.youtube_video_downloader_cls,
        'download',
        return_value=open('test.mp4', 'w').name
    )
    next_stage = youtube_downloader_conversation.download_video(
        telegram_update, telegram_context)
    assert not os.path.exists('test.mp4')
    assert next_stage == ConversationHandler.END
    assert send_video_mocker.called
    assert send_video_mocker.call_args.kwargs['video_file_path'] == 'test.mp4'


def test_download_mp4_failure(
    mocker: MockerFixture,
    youtube_downloader_conversation: YoutubeDownloaderConversation,
    telegram_update: Update,
    telegram_context: CallbackContext
):
    """
    Given:
     - mp4 requested format
     - download operation to mp4 which failed.
     - YouTube object with valid URL

    When:
     - executing the 'download_video' stage

    Then:
     - make sure an exception is raised.
    """
    def throw_exception():
        raise Exception('could not download youtube video as mp4')

    mocker.patch.object(youtube_downloader_conversation.telegram_service,
                        'get_message_data', return_value='mp4')
    mocker.patch.object(
        youtube_downloader_conversation.telegram_service, 'edit_message')

    mocker.patch.object(
        youtube_downloader_conversation.youtube_video_downloader_cls,
        'download',
        side_effect=throw_exception
    )

    telegram_context.user_data['youtube'] = YouTube(
        'https://www.youtube.com/watch?v=rn9AQoI7mYU&list=RD7pKrVB5f2W0&index=5'
    )

    with pytest.raises(YouTubeVideoDownloadError) as excinfo:
        youtube_downloader_conversation.download_video(
            telegram_update, telegram_context
        )

    assert excinfo.value.args[0] == 'Failed to download YouTube video https://youtube.com/watch?v=rn9AQoI7mYU as mp4'
