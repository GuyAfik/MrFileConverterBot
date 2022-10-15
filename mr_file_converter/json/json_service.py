import os
from contextlib import contextmanager
from typing import Generator

from mr_file_converter.command.command_service import CommandService
from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.io.io_service import IOService


class JsonService:

    def __init__(
        self,
        command_service: CommandService,
        io_service: IOService,
        json_converter: JsonConverter,
        yml_converter: YamlConverter,
        xml_converter: XMLConverter
    ):
        self.command_service = command_service
        self.io_service = io_service
        self.json_converter = json_converter
        self.yml_converter = yml_converter
        self.xml_converter = xml_converter

    @contextmanager
    def to_yml(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        """
        Converts json to yml file.
        """
        with self.io_service.create_temp_yml_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as destination_file_path:
            self.yml_converter.write(
                data=self.json_converter.read(source_file_path),
                file_path=destination_file_path
            )
            yield destination_file_path

    @contextmanager
    def to_string(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        """
        Converts json to a file that is a string representation of the json.
        """
        with self.io_service.create_temp_txt_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as destination_file_path:
            self.io_service.write_data_to_file(
                data=self.json_converter.dumps(
                    self.json_converter.read(source_file_path)),
                file_path=destination_file_path
            )
            yield destination_file_path

    @contextmanager
    def to_xml(self, source_file_path: str, custom_file_name: str | None = None) -> Generator[str, None, None]:
        with self.io_service.create_temp_xml_file(
            prefix=custom_file_name or os.path.splitext(source_file_path)[0]
        ) as xml_file:
            self.xml_converter.write(
                data=self.json_converter.read(source_file_path),
                file_path=xml_file
            )
            yield xml_file
