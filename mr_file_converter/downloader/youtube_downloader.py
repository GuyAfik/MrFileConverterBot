import logging
import os

from pytube import YouTube
from telegram import Update
from telegram.ext import ConversationHandler

from mr_file_converter.telegram.telegram_service import TelegramService

logger = logging.getLogger(__name__)


class YouTubeDownloader:

    def __init__(self, youtube: YouTube, telegram_service: TelegramService):
        self._youtube = youtube
        self._telegram_service = telegram_service
        self._path = None

    @property
    def path(self):
        return self._path

    def __enter__(self):
        pass

    def send(self, update: Update) -> int:
        pass

    def download(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self._path):
            os.remove(self._path)


class YouTubeVideoDownloader(YouTubeDownloader):
    """
    Downloads a YouTube video and deletes it once it has been used. Must be used as a context manager.
    """

    def __enter__(self):
        # returns a file object that the video was downloaded into.
        try:
            self._path = self.download()
            return self
        except Exception as e:
            logger.error(
                f'Could not download youtube video {self._youtube.watch_url}. Error:\n{e}')
            raise e

    def send(self, update: Update) -> int:
        self._telegram_service.send_video(
            update=update,
            video_file_path=self._path,  # type: ignore
            reply_to_message_id=self._telegram_service.get_message_id(update)
        )
        return ConversationHandler.END

    def download(self):
        return self._youtube.streams.get_highest_resolution().download()


class YouTubeAudioDownloader(YouTubeDownloader):
    """
    Downloads a YouTube audio and deletes it once it has been used. Must be used as a context manager.
    """

    def __enter__(self):
        try:
            self._path = self.download()
            base, _ = os.path.splitext(self._path)
            new_file = f'{base}.mp3'
            # due to pytube bug, rename the file to be .mp3 file
            os.rename(self._path, new_file)
            self._path = new_file
            return self
        except Exception as e:
            logger.error(
                f'Could not download youtube audio {self._youtube.watch_url}. Error:\n{e}')
            raise e

    def send(self, update: Update) -> int:
        self._telegram_service.send_audio(
            update=update,
            audio_file_path=self._path,  # type: ignore
            reply_to_message_id=self._telegram_service.get_message_id(update)
        )
        return ConversationHandler.END

    def download(self):
        return self._youtube.streams.get_audio_only().download()
