import logging
import os
from contextlib import contextmanager
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import Generator

logger = logging.getLogger(__name__)


class IOService:

    def __init__(self):
        self.temporary_directory = TemporaryDirectory
        self.named_temporary_file = NamedTemporaryFile

    @staticmethod
    def remove_file(file_name: str):
        if os.path.exists(file_name):
            os.remove(file_name)

    @contextmanager
    def create_temp_directory(self) -> Generator[str, None, None]:
        try:
            temporary_directory = self.temporary_directory()
            yield temporary_directory.name
        except Exception as e:
            logger.error('failed to create temp directory')
            raise e

        temporary_directory.cleanup()
        self.remove_file(temporary_directory.name)

    @contextmanager
    def create_temp_file(
        self, prefix: str | None = None, suffix: str | None = None, should_delete: bool = True
    ) -> Generator[str, None, None]:

        if suffix and '.' not in suffix:
            suffix = f'.{suffix}'

        try:
            temporary_file = self.named_temporary_file(
                prefix=prefix, suffix=suffix, delete=should_delete
            )
            file_name = f'{prefix}{suffix}'
            os.rename(temporary_file.name, file_name)
            yield file_name
        except Exception as e:
            logger.error(f'failed to create temp file {prefix}{suffix}')
            raise e
        finally:
            os.rename(file_name, temporary_file.name)
            temporary_file.close()
            self.remove_file(temporary_file.name)

    @contextmanager
    def create_temp_json_file(self, prefix: str) -> Generator[str, None, None]:
        with self.create_temp_file(prefix=prefix, suffix=".json") as out_path:
            yield out_path

    @contextmanager
    def create_temp_yml_file(self, prefix: str) -> Generator[str, None, None]:
        with self.create_temp_file(prefix=prefix, suffix=".yml") as out_path:
            yield out_path

    @contextmanager
    def create_temp_png_file(self, prefix: str) -> Generator[str, None, None]:
        try:
            with self.create_temp_file(prefix=prefix, suffix=".png") as out_path:
                yield out_path
        finally:
            pass

    @contextmanager
    def create_temp_jpg_file(self, prefix: str) -> Generator[str, None, None]:
        with self.create_temp_file(prefix=prefix, suffix=".jpg") as out_path:
            yield out_path

    @contextmanager
    def create_temp_txt_file(self, prefix: str) -> Generator[str, None, None]:
        try:
            with self.create_temp_file(prefix=prefix, suffix=".txt") as out_path:
                yield out_path
        finally:
            pass

    @contextmanager
    def create_temp_pdf_file(self, prefix: str) -> Generator[str, None, None]:
        with self.create_temp_file(prefix=prefix, suffix='.pdf') as out_path:
            yield out_path

    @contextmanager
    def create_temp_xml_file(self, prefix: str) -> Generator[str, None, None]:
        with self.create_temp_file(prefix=prefix, suffix='.xml') as out_path:
            yield out_path

    @contextmanager
    def create_temp_html_file(self, prefix: str) -> Generator[str, None, None]:
        with self.create_temp_file(prefix=prefix, suffix='.html') as out_path:
            yield out_path

    @staticmethod
    def write_data_to_file(data: str, file_path: str, mode: str = 'w'):
        with open(file_path, mode) as file:
            file.write(data)
