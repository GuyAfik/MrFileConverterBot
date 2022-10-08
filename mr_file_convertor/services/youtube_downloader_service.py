from abc import abstractmethod

import os
import logging
from pytube import YouTube

logger = logging.getLogger(__name__)


class YouTubeDownloader:

    def __init__(self, url: str):
        try:
            self._youtube = YouTube(url)
        except Exception:
            error_msg = f'invalid YouTube video URL {url}'
            logger.error(error_msg)
            raise ValueError(error_msg)
        self.__path = None

    @abstractmethod
    def send(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.exists(self.__path):
            os.remove(self.__path)


class YouTubeVideoDownloader(YouTubeDownloader):
    """
    Downloads a YouTube video and deletes it once it has been used. Must be used as a context manager.
    """

    def __enter__(self):
        # returns a file object that the video was downloaded into.
        try:
            self.__path = self._youtube.streams.get_highest_resolution().download()
            return open(self.__path, 'rb')
        except Exception as e:
            logger.error(f'Could not download youtube video {self._youtube.watch_url}. Error:\n{e}')
            raise e

    def send(self):
        pass


class YouTubeAudioDownloader(YouTubeDownloader):

    def __enter__(self):
        try:
            self.__path = self._youtube.streams.filter(only_video=True).first().download()
            return open(self.__path, 'rb')
        except Exception as e:
            logger.error(f'Could not download youtube audio {self._youtube.watch_url}. Error:\n{e}')
            raise e

    def send(self):
        pass
