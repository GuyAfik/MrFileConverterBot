import logging

from pytube import YouTube
from telegram import Update
from telegram.ext import CallbackContext

from mr_file_converter.command.command_service import CommandService
from mr_file_converter.downloader.youtube_downloader import (
    YouTubeAudioDownloader, YouTubeDownloader, YouTubeVideoDownloader)
from mr_file_converter.telegram.telegram_service import TelegramService

logger = logging.getLogger(__name__)


class YoutubeDownloaderService:

    check_youtube_url_stage, download_stage = range(2)

    def __init__(self, telegram_service: TelegramService, command_service: CommandService):
        self.telegram_service = telegram_service
        self.command_service = command_service
        self.youtube_audio_downloader_cls = YouTubeAudioDownloader
        self.youtube_video_downloader_cls = YouTubeVideoDownloader

    def ask_youtube_url(self, update: Update, context: CallbackContext):
        self.telegram_service.send_message(
            update, text=f'Please enter the youtube URL')
        return self.check_youtube_url_stage

    def check_youtube_url(self, update: Update, context: CallbackContext):
        url = self.telegram_service.get_message_data(update)
        try:
            context.user_data['youtube'] = YouTube(url)
            return self.choose_audio_or_video(update)
        except Exception as e:
            logger.error(f'invalid YouTube video URL {url}, error: {e}')
            self.telegram_service.reply_to_message(
                update, text=f'The url {url} is invalid, please enter a valid url.'
            )
            return self.check_youtube_url_stage

    def choose_audio_or_video(self, update: Update):
        self.telegram_service.send_message(
            update,
            text='Please choose in which format would you like to get the youtube video?',
            reply_markup=self.telegram_service.get_inline_keyboard(
                buttons=['mp3', 'mp4']
            )
        )
        return self.download_stage

    def download_video(self, update: Update, context: CallbackContext):
        _format = self.telegram_service.get_message_data(update)
        self.telegram_service.edit_message(
            update, text=f'Please hang on while I am bring to you the video in {_format} format...🤔'
        )

        with self.youtube_downloader_factory(context, _format) as youtube_downloader:
            return youtube_downloader.send(update)

    def youtube_downloader_factory(self, context: CallbackContext, _type: str) -> YouTubeDownloader:

        youtube: YouTube = context.user_data.get('youtube')

        if _type not in ('mp3', 'mp4'):
            raise ValueError(f'type {_type} must be mp3/mp4 only.')

        type_to_class = {
            'mp3': self.youtube_audio_downloader_cls,
            'mp4': self.youtube_video_downloader_cls
        }

        return type_to_class[_type](youtube, self.telegram_service)
