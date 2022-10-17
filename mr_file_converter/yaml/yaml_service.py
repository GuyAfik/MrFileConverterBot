import os
from contextlib import contextmanager
from typing import Generator

from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.io.io_service import IOService


class YamlService:

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

    @contextmanager
    def to_json(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        """
        Converts json to yml file.
        """
        with self.io_service.create_temp_json_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as json_file:
            self.json_converter.write(
                data=self.yml_converter.read(source_file_path),
                file_path=json_file
            )
            yield json_file

    @contextmanager
    def to_text(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        """
        Converts yml to a file that is a string representation of the yml.
        """
        with self.io_service.create_temp_txt_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as text_file:
            self.io_service.write_data_to_file(
                data=self.yml_converter.dumps(
                    self.yml_converter.read(source_file_path)),
                file_path=text_file
            )
            yield text_file

    @contextmanager
    def to_xml(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        with self.io_service.create_temp_xml_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as xml_file:
            self.xml_converter.write(
                data=self.yml_converter.read(source_file_path),
                file_path=xml_file
            )
            yield xml_file
