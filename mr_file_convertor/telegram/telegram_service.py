from typing import List

from telegram import (Bot, CallbackQuery, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message, ReplyMarkup, Update)
from telegram.ext import CallbackContext, ConversationHandler, Updater
from telegram.utils.types import ODVInput


class TelegramService:
    def __init__(self, updater: Updater | None = None, bot: Bot | None = None):
        self.bot = bot or updater.bot  # type: ignore

    @staticmethod
    def get_callback_query(update: Update) -> CallbackQuery | None:
        return update.callback_query

    def get_message(self, update: Update, reply_to_message_id: bool = False) -> Message:
        if callback_query := self.get_callback_query(update):
            return callback_query.message

        if reply_to_message_id:
            return update.effective_message.reply_to_message

        return update.effective_message

    def get_message_id(self, update: Update, reply_to_message_id: bool = False) -> int:
        return self.get_message(update, reply_to_message_id).message_id

    def get_chat_id(self, update: Update, reply_to_message_id: bool = False) -> int:
        return self.get_message(update, reply_to_message_id).chat_id

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
        return self.get_message(
            update, reply_to_message_id=True
        ).reply_text(text=text, parse_mode=parse_mode, reply_markup=reply_markup)

    def get_message_data(self, update: Update) -> str:
        if callback_query := self.get_callback_query(update):
            return callback_query.data
        return self.get_message(update).text

    def cancel(self, update: Update, context: CallbackContext):
        return self.help(update, context)

    def help(self, update: Update, context: CallbackContext):
        first_name = context.bot.first_name
        last_name = context.bot.last_name
        self.send_message(
            update, text=f'Hi, {first_name} {last_name}, show here the help command...')
        return ConversationHandler.END
