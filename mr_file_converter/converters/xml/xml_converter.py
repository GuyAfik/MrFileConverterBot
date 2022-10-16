import logging
from typing import Any

import xmltodict
from dict2xml import dict2xml

from mr_file_converter.converters.base_converter import BaseConverter

logger = logging.getLogger(__name__)


class XMLConverter(BaseConverter):

    def read(self, file_path: str):
        try:
            with open(file_path, 'r') as xml_file:
                xml_input = xml_file.read().strip().replace('\n', '').replace('\r', '')
                return xmltodict.parse(xml_input=xml_input)
        except Exception as e:
            logger.error(f'failed to read XML file {file_path}, error:\n{e}')
            raise e

    def write(self, data: Any, file_path: str):
        try:
            with open(file_path, 'w') as file:
                xml = '<?xml version="1.0" encoding="UTF-8" ?>'
                file.write(f"{xml}\n{dict2xml(data, wrap='root')}")
        except Exception as e:
            logger.error(
                f'failed to parse {file_path} to XML file, error:\n{e}')
            raise e
