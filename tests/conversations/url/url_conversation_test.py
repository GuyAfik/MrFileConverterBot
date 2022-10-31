
import pytest
from pytest_mock import MockerFixture
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler

from mr_file_converter.conversations.url.url_conversation import \
    URLConversation
from mr_file_converter.services.telegram.telegram_service import \
    TelegramService
from mr_file_converter.services.url.errors import (InvalidURL,
                                                   URLToFileConversionError)
from mr_file_converter.services.url.url_service import URLService


@pytest.fixture()
def url_conversation(
    url_service: URLService, telegram_service: TelegramService
) -> URLConversation:
    return URLConversation(
        telegram_service=telegram_service,
        url_service=url_service
    )


def test_check_url_validity_with_valid_url(
    mocker: MockerFixture,
    url_conversation: URLConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
):
    """
    Given:
     - google URL.

    When:
     - running 'check_url_validity' method

    Then:
     - make sure the next stage is the 'ask_file_name_stage'
     - make sure the reply message is called to show the available file formats
     - make sure the url is saved in context for later stages in the conversation
    """
    mocker.patch.object(
        url_conversation.telegram_service,
        'get_message_data',
        return_value='https://www.google.com/'
    )

    reply_message_mocker = mocker.patch.object(
        url_conversation.telegram_service, 'reply_to_message'
    )
    next_stage = url_conversation.check_url_validity(
        telegram_update, telegram_context)
    assert telegram_context.user_data['url'] == 'https://www.google.com/'
    assert reply_message_mocker.called
    assert next_stage == url_conversation.ask_file_name_stage


@pytest.mark.parametrize(
    'invalid_url',
    [
        'skfddkff',
        'vbmvfmsd',
        'walla',
        'google',
        'test',
        'httpss://google.com',
        'bla.com',
    ]
)
def test_check_url_validity_with_random_strings(
    mocker: MockerFixture,
    url_conversation: URLConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
    invalid_url: str
):
    """
    Given:
     - invalid URLs

    When:
     - running 'check_url_validity' method

    Then:
     - make sure the InvalidURL exception is raised
     - make sure the 'url' key is not in the context
     - make sure the next stage is the 'check_url_validity_stage' (same one)
     - make sure the exception error is correct
    """
    mocker.patch.object(
        url_conversation.telegram_service,
        'get_message_data',
        return_value=invalid_url
    )

    with pytest.raises(InvalidURL) as exc_info:
        url_conversation.check_url_validity(telegram_update, telegram_context)

    assert 'url' not in telegram_context.user_data
    assert exc_info.value.next_stage == url_conversation.check_url_validity_stage
    assert exc_info.value.args[0] == f'the url {invalid_url} is invalid, please enter a valid url'


def test_check_url_validity_with_http_error(
    mocker: MockerFixture,
    url_conversation: URLConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
):
    """
    Given:
     - valid URL which cannot be read due to HTTP error

    When:
     - running 'check_url_validity' method

    Then:
     - make sure the InvalidURL exception is raised
     - make sure the 'url' key is not in the context
     - make sure the next stage is the 'check_url_validity_stage' (same one)
     - make sure the exception error is correct
    """
    def throw_exception(url, context=None):
        raise Exception(f'HTTP error for {url}')

    mocker.patch.object(
        url_conversation.telegram_service,
        'get_message_data',
        return_value='a real url'
    )

    mocker.patch.object(
        url_conversation,
        'urlopen',
        side_effect=throw_exception
    )

    with pytest.raises(InvalidURL) as exc_info:
        url_conversation.check_url_validity(telegram_update, telegram_context)

    assert 'url' not in telegram_context.user_data
    assert exc_info.value.next_stage == url_conversation.check_url_validity_stage
    assert exc_info.value.args[0] == f'Unable to read a real url, please try a different url'


@pytest.mark.parametrize(
    'invalid_youtube_urls',
    [
        ['a'],
        ['a', 'b'],
        ['a', 'b', 'c']
    ]
)
def test_check_url_validity_multiple_invalid_urls(
    mocker: MockerFixture,
    url_conversation: URLConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
    invalid_youtube_urls: list
):
    """
    Given:
     - invalid URLs that user put and finally a valid url

    When:
     - running 'check_url_validity' method

    Then:
     - make sure the InvalidURL exception is raised whenever the URL is invalid
     - make sure the 'url' key is not in the context when an exception is raised
     - make sure the next stage is ask_file_name_stage when the URL is valid
     - make sure the url is saved at context when there is no exception
    """
    mocker.patch.object(
        url_conversation.telegram_service,
        'get_message_data',
        side_effect=invalid_youtube_urls + [
            'https://www.google.com/'
        ]
    )

    reply_message_mocker = mocker.patch.object(
        url_conversation.telegram_service, 'reply_to_message'
    )

    for _ in range(len(invalid_youtube_urls)):
        with pytest.raises(InvalidURL):
            url_conversation.check_url_validity(
                update=telegram_update, context=telegram_context
            )
            assert 'url' not in telegram_context.user_data

    next_stage = url_conversation.check_url_validity(
        telegram_update, telegram_context
    )
    assert telegram_context.user_data['url'] == 'https://www.google.com/'
    assert reply_message_mocker.called
    assert next_stage == url_conversation.ask_file_name_stage


@pytest.mark.parametrize(
    'requested_format',
    [
        'pdf',
        'html',
        'jpg',
        'png'
    ]
)
def test_convert_url_success(
    mocker: MockerFixture,
    url_conversation: URLConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
    requested_format: str
):
    """
    Given:
     - requested URL formats with Google URL.

    When:
     - running 'convert_url' method

    Then:
     - make sure the next stage is the 'convert_additional_url_stage'
     - make sure the file was sent
     - make sure a message to convert additional url was sent
     - make sure the file-name that is being sent is correct
    """
    telegram_context.user_data['requested_format'] = requested_format
    telegram_context.user_data['url'] = 'https://www.google.com/'
    mocker.patch.object(
        url_conversation.telegram_service,
        'get_message_data',
        return_value='test'
    )

    send_file_mocker = mocker.patch.object(
        url_conversation.telegram_service,
        'send_file',
        return_value='test'
    )

    send_message_mocker = mocker.patch.object(
        url_conversation.telegram_service,
        'send_message',
        return_value='test'
    )

    next_stage = url_conversation.convert_url(
        telegram_update, telegram_context
    )

    assert next_stage == url_conversation.convert_additional_url_stage
    assert send_file_mocker.called
    assert send_file_mocker.call_args.kwargs['file_name'] == f'test.{requested_format}'
    assert send_message_mocker.called


@pytest.mark.parametrize(
    'mock_function, requested_format',
    [
        (
            'to_pdf', 'pdf'
        ),
        (
            'to_html', 'html'
        ),
        (
            'to_png', 'png'
        ),
        (
            'to_jpg', 'jpg'
        )
    ]
)
def test_convert_url_failure(
    mocker: MockerFixture,
    url_conversation: URLConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
    mock_function: str,
    requested_format: str
):
    """
    Given:
     - requested format to convert into
     - an error that occurred during conversation

    When:
     - running 'convert_url' method

    Then:
     - make sure the next stage is the 'ConversationHandler.END'
     - make sure the URLToFileConversionError exception was raised
     - make sure the correct error message is set
    """
    def error_side_effect(url, custom_file_name):
        raise Exception(f'Failed to turn {url} into {custom_file_name}')

    telegram_context.user_data['requested_format'] = requested_format
    telegram_context.user_data['url'] = 'https://www.google.com/'
    mocker.patch.object(
        url_conversation.telegram_service,
        'get_message_data',
        return_value='test'
    )
    mocker.patch.object(
        url_conversation.url_service, mock_function, side_effect=error_side_effect
    )

    with pytest.raises(URLToFileConversionError) as exc_info:
        url_conversation.convert_url(telegram_update, telegram_context)

    assert exc_info.value.next_stage == ConversationHandler.END
    assert exc_info.value.args[0] == f'Error when converting URL https://www.google.com/' \
                                     f' to target file format {requested_format}'


def test_convert_additional_file_yes_option(
    mocker: MockerFixture,
    url_conversation: URLConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
):
    """
    Given:
     - 'yes' marked option to get additional file from url

    When:
     - running 'convert_additional_file_answer' method

    Then:
     - make sure the next stage is the 'check_url_validity_stage' (first stage in the conversation)
    """
    mocker.patch.object(
        url_conversation.telegram_service,
        'get_message_data',
        return_value='yes'
    )
    send_message_mocker = mocker.patch.object(
        url_conversation.telegram_service, 'send_message'
    )

    next_stage = url_conversation.convert_additional_url_answer(
        telegram_update, telegram_context
    )

    assert send_message_mocker.called
    assert next_stage == url_conversation.check_url_validity_stage


def test_convert_additional_file_no_option(
    mocker: MockerFixture,
    url_conversation: URLConversation,
    telegram_update: Update,
    telegram_context: CallbackContext,
):
    """
    Given:
     - 'no' marked option to get additional file from url

    When:
     - running 'convert_additional_file_answer' method

    Then:
     - make sure the next stage is the 'ConversationHandler.END'
    """
    mocker.patch.object(
        url_conversation.telegram_service,
        'get_message_data',
        return_value='no'
    )
    edit_message_mocker = mocker.patch.object(
        url_conversation.telegram_service, 'edit_message'
    )

    next_stage = url_conversation.convert_additional_url_answer(
        telegram_update, telegram_context
    )

    assert edit_message_mocker.called
    assert next_stage == ConversationHandler.END
