from typing import List, cast
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture
from telegram import CallbackQuery, Document, Message, PhotoSize, Update
from telegram.ext import CallbackContext

from mr_file_converter.services.telegram.telegram_service import \
    TelegramService


@pytest.fixture()
def telegram_document() -> Document:
    document = cast(Document, MagicMock())
    document.file_id = 'document_123'
    return document


@pytest.fixture()
def telegram_photo() -> List[PhotoSize]:
    photo = cast(PhotoSize, MagicMock())
    photo.file_id = 'photo_123'
    return [photo]


@pytest.fixture()
def telegram_message() -> Message:
    return cast(Message, MagicMock())


@pytest.fixture()
def telegram_message_with_document(
    telegram_message: Message, telegram_document: Document
) -> Message:
    telegram_message.document = telegram_document
    return telegram_message


@pytest.fixture()
def telegram_message_with_photo(
    telegram_message: Message, telegram_photo: List[PhotoSize]
) -> Message:
    telegram_message.photo = telegram_photo
    telegram_message.document = None
    return telegram_message


@pytest.fixture()
def telegram_callback_query(telegram_message: Message) -> CallbackQuery:
    callback_query = cast(CallbackQuery, MagicMock())
    message = telegram_message
    message.message_id = 'callback_query_message_id'
    callback_query.message = message
    return callback_query


def test_get_document_file(
    mocker: MockerFixture,
    telegram_service: TelegramService,
    telegram_message_with_document: Message,
    telegram_update: Update,
    telegram_context: CallbackContext
):
    """
    Given:
    - a document from a message

    When:
    - trying to download the document file

    Then:
    - make sure the downloaded file was called with the document id
    """
    get_file_mocker = mocker.patch.object(
        telegram_service.bot,
        'get_file'
    )

    telegram_update.effective_message = telegram_message_with_document

    telegram_service.get_file(telegram_update)
    assert get_file_mocker.call_args.kwargs == {'file_id': 'document_123'}


def test_get_photo_file(
    mocker: MockerFixture,
    telegram_service: TelegramService,
    telegram_message_with_photo: Message,
    telegram_update: Update,
    telegram_context: CallbackContext
):
    """
    Given:
    - a photo from a message

    When:
    - trying to download the photo file

    Then:
    - make sure the downloaded file was called with the photo id
    """
    get_file_mocker = mocker.patch.object(
        telegram_service.bot,
        'get_file'
    )

    telegram_update.effective_message = telegram_message_with_photo
    telegram_service.get_file(telegram_update)
    assert get_file_mocker.call_args.kwargs == {'file_id': 'photo_123'}


def test_get_effective_message(
    telegram_service: TelegramService,
    telegram_message: Message,
    telegram_update: Update,
):
    """
    Given:
    - an effective message

    When:
    - trying to retrieve the correct message (effective message)

    Then:
    - make sure the effective message is returned
    """
    telegram_message.message_id = 'effective_message_123'
    telegram_update.effective_message = telegram_message
    assert telegram_service.get_message(
        telegram_update
    ).message_id == 'effective_message_123'


def test_get_message(
    telegram_service: TelegramService,
    telegram_message: Message,
    telegram_update: Update,
):
    """
    Given:
    - a message

    When:
    - trying to retrieve the correct message

    Then:
    - make sure the message is returned when there is no 'effective_message'
    """
    telegram_message.message_id = 'message_123'
    telegram_update.message = telegram_message
    telegram_update.effective_message = None
    assert telegram_service.get_message(
        telegram_update
    ).message_id == 'message_123'


def test_get_callback_query(
    telegram_service: TelegramService,
    telegram_callback_query: CallbackQuery,
    telegram_update: Update,
):
    """
    Given:
    - a callback query with a message

    When:
    - trying to retrieve the message from the callback query

    Then:
    - make sure the message of the callback query is returned
    """
    telegram_update.callback_query = telegram_callback_query
    assert telegram_service.get_message(
        telegram_update
    ).message_id == 'callback_query_message_id'
