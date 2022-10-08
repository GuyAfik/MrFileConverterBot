import logging
import os
from abc import ABC, abstractmethod

from pytube import YouTube

logger = logging.getLogger(__name__)


class YouTubeDownloader(ABC):

    def __init__(self, url: str):
        try:
            self._youtube = YouTube(url)
        except Exception:
            error_msg = f'invalid YouTube video URL {url}'
            logger.error(error_msg)
            raise ValueError(error_msg)
        self._path = None

    @abstractmethod
    def send(self):
        pass

    def __enter__(self):
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
            self._path = self._youtube.streams.get_highest_resolution().download()
            return open(self._path, 'rb')
        except Exception as e:
            logger.error(
                f'Could not download youtube video {self._youtube.watch_url}. Error:\n{e}')
            raise e

    def send(self):
        pass


class YouTubeAudioDownloader(YouTubeDownloader):
    """
    Downloads a YouTube audio and deletes it once it has been used. Must be used as a context manager.
    """

    def __enter__(self):
        try:
            self._path = self._youtube.streams.get_audio_only().download()
            base, _ = os.path.splitext(self._path)
            new_file = base + '.mp3'
            # due to pytube bug, rename the file to be .mp3 file
            os.rename(self._path, new_file)
            self._path = new_file
            return open(self._path, 'rb')
        except Exception as e:
            logger.error(
                f'Could not download youtube audio {self._youtube.watch_url}. Error:\n{e}')
            raise e

    def send(self):
        pass
