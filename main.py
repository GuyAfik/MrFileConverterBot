from mr_file_convertor.services.youtube_downloader_service import YouTubeAudioDownloader


if __name__ == '__main__':
    with YouTubeAudioDownloader(url='https://www.youtube.com/watch?v=3YasCzybyt4&list=RD3YasCzybyt4&start_radio=1') as f:
        print()
