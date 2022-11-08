import io
import logging
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from mr_file_converter.converters.base_converter import BaseConverter

logger = logging.getLogger(__name__)


class RueamelYamlConverter(BaseConverter):

    def __init__(self):
        self.yml = YAML()

    def loads(self, data: str) -> object:
        return self.yml.load(data)

    def dumps(self, obj: object) -> str:
        buf = io.StringIO()
        self.yml.dump(obj, buf)
        return buf.getvalue()

    def read(self, file_path: str):
        try:
            return self.yml.load(Path(file_path))
        except ValueError as e:
            logger.error(f'Failed to load YAML file {file_path}, error: {e}')
            raise e

    def write(self, data: Any, file_path: str):
        try:
            with open(file_path, 'w') as file:
                self.yml.dump(data, file)
        except ValueError as e:
            logger.error(
                f'Failed to write {data} into YAML file {file_path}, error: {e}'
            )
            raise e
