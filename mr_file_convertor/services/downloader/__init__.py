
from typing import Optional, Union

from mr_file_convertor.services.downloader.youtube_downloader import (
    YouTubeAudioDownloader, YouTubeDownloader, YouTubeVideoDownloader)


def youtube_downloader_factory(url: str, _type: str) -> Optional[Union[YouTubeAudioDownloader, YouTubeVideoDownloader]]:
    if _type not in ('mp3', 'mp4'):
        raise ValueError(f'type {_type} must be mp3/mp4 only.')

    if _type == 'mp3':
        return YouTubeAudioDownloader(url)
    elif _type == 'mp4':
        return YouTubeVideoDownloader(url)

    return None
