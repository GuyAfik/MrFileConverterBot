
import pytest
from pytest_mock import MockerFixture
from telegram import Update
from telegram.ext import CallbackContext

from mr_file_converter.conversations.url.errors import InvalidURL
from mr_file_converter.conversations.url.url_conversation import \
    URLConversation
from mr_file_converter.services.telegram.telegram_service import \
    TelegramService
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
        url_conversation.telegram_service, 'reply_to_message')
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
