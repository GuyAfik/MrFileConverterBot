from mr_file_converter.command.command_service import CommandService
from mr_file_converter.converters import (JsonConverter, XMLConverter,
                                          YamlConverter)
from mr_file_converter.io.io_service import IOService


class XMLService:

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
