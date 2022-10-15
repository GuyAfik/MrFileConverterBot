import logging
from typing import Any, Union
from xml.etree import ElementTree
from mr_file_converter.converters.base_converter import BaseConverter
import xmltodict
from dict2xml import dict2xml

logger = logging.getLogger(__name__)


class XMLConverter(BaseConverter):

    def read(self, file_path: str, as_element: bool = False) -> ElementTree.ElementTree | dict:
        try:
            if as_element:
                return ElementTree.parse(file_path)

            with open(file_path, 'r') as xml_file:
                return xmltodict.parse(xml_input=xml_file)
        except Exception as e:
            logger.error(f'failed to read XML file {file_path}, error:\n{e}')
            raise e

    def write(self, data: Any, file_path: str):
        try:
            with open(file_path, 'w') as file:
                file.write(dict2xml(data, indent="  "))
        except Exception as e:
            logger.error(f'failed to parse {file_path} to XML file, error:\n{e}')
            raise e