import logging
from typing import Any

import ujson  # type: ignore

from mr_file_converter.converters.base_converter import BaseConverter

logger = logging.getLogger(__name__)


class UJsonConverter(BaseConverter):

    def __init__(self):
        self.json = ujson

    def read(self, file_path: str):
        try:
            with open(file_path) as file:
                return self.json.load(file)
        except ValueError as e:
            logger.error(f'Failed to load JSON file {file_path}, error: {e}')
            raise e

    def write(self, data: Any, file_path: str):
        try:
            with open(file_path, 'w') as file:
                ujson.dump(data, file)
        except ValueError as e:
            logger.error(
                f'Failed to write {data} into JSON file {file_path}, error: {e}')
            raise e
