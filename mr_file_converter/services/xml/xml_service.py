import os
from contextlib import contextmanager
from typing import Generator

from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.services.io.io_service import IOService


class XMLService:

    def __init__(
        self,
        io_service: IOService,
        json_converter: JsonConverter,
        yml_converter: YamlConverter,
        xml_converter: XMLConverter
    ):
        self.io_service = io_service
        self.json_converter = json_converter
        self.yml_converter = yml_converter
        self.xml_converter = xml_converter

    def get_xml_file_content(self, source_file_path: str):
        xml_file_as_dict: dict = self.xml_converter.read(source_file_path)
        if 'root' in xml_file_as_dict and len(xml_file_as_dict.keys()) == 1:
            xml_file_as_dict = xml_file_as_dict.pop('root')
        return xml_file_as_dict

    @contextmanager
    def to_json(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        """
        Converts xml to json file.
        """
        with self.io_service.create_temp_json_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as json_file:
            self.json_converter.write(
                data=self.get_xml_file_content(source_file_path),
                file_path=json_file
            )
            yield json_file

    @contextmanager
    def to_yml(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        """
        Converts xml to yml file.
        """
        with self.io_service.create_temp_yml_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as yml_file:
            self.yml_converter.write(
                data=self.get_xml_file_content(source_file_path),
                file_path=yml_file
            )
            yield yml_file
