from typing import IO, List, Tuple, Union

from telegram import (Bot, CallbackQuery, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message, ReplyMarkup, Update)
from telegram.ext import CallbackContext, Updater
from telegram.utils.types import ODVInput


class TelegramService:
    """
    This service is responsible for the communication with the telegram bot api as well as to provide any telegram
    object that can be utilized in other services.
    """

    def __init__(self, updater: Updater | None = None, bot: Bot | None = None):
        self.bot = bot or updater.bot  # type: ignore

    @staticmethod
    def get_callback_query(update: Update) -> CallbackQuery | None:
        return update.callback_query

    def get_message(self, update: Update, reply_to_message_id: bool = False) -> Message:
        if callback_query := self.get_callback_query(update):
            return callback_query.message

        if reply_to_message_id:
            return update.effective_message.reply_to_message or update.message.reply_to_message

        return update.effective_message or update.message

    def get_message_id(self, update: Update, reply_to_message_id: bool = False) -> int:
        return self.get_message(update, reply_to_message_id).message_id

    def get_chat_id(self, update: Update, reply_to_message_id: bool = False) -> int:
        return self.get_message(update, reply_to_message_id).chat_id

    def get_user_first_and_last_name(self, update: Update) -> Tuple[str, str]:
        message = self.get_message(update)
        return message.from_user.first_name, message.from_user.last_name

    @staticmethod
    def get_inline_keyboard(buttons: List[str]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=button, callback_data=button) for button in buttons
                ]
            ]
        )

    def send_message(
        self, update: Update, text: str, parse_mode: ODVInput[str] = None, reply_markup: ReplyMarkup = None
    ) -> Message:
        return self.bot.send_message(
            chat_id=self.get_chat_id(update), text=text, parse_mode=parse_mode, reply_markup=reply_markup
        )

    def reply_to_message(
        self, update: Update, text: str, parse_mode: ODVInput[str] = None, reply_markup: ReplyMarkup = None
    ) -> Message:
        return self.get_message(update).reply_text(
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            reply_to_message_id=self.get_message_id(update)
        )

    def edit_message(self, update: Update, text: str) -> Union[Message, bool]:
        return self.bot.edit_message_text(
            text=text,
            chat_id=self.get_chat_id(update),
            message_id=self.get_message_id(update)
        )

    def get_message_data(self, update: Update) -> str:
        if callback_query := self.get_callback_query(update):
            return callback_query.data
        return self.get_message(update).text

    def get_file(self, update: Update, context: CallbackContext) -> Union[str, IO]:
        message = self.get_message(update)
        file_id = message.document.file_id if message.document else message.photo[0].file_id
        return context.bot.get_file(file_id=file_id).download()

    def send_file(self, update: Update, document_path: str) -> Message:
        with open(document_path, 'rb') as document:
            return self.bot.send_document(
                chat_id=self.get_chat_id(update),
                document=document
            )

    def send_audio(self, update: Update, audio_file_path: str, reply_to_message_id: int | None = None) -> Message:
        with open(audio_file_path, 'rb') as audio:
            return self.bot.send_audio(
                chat_id=self.get_chat_id(update),
                audio=audio,  # type: ignore
                reply_to_message_id=reply_to_message_id
            )

    def send_video(self, update: Update, video_file_path: str, reply_to_message_id: int | None = None) -> Message:
        with open(video_file_path, 'rb') as video:
            return self.bot.send_video(
                chat_id=self.get_chat_id(update),
                video=video,  # type: ignore
                reply_to_message_id=reply_to_message_id
            )
