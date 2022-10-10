
from mr_file_converter.command.command_service import CommandService
from mr_file_converter.converters import JsonConverter, YamlConverter


class JsonService:

    def __init__(self, command_service: CommandService, json_converter: JsonConverter, yml_converter: YamlConverter):
        self.command_service = command_service
        self.json_converter = json_converter
        self.yml_converter = yml_converter

    def to_yml(self, source_file_path: str, destination_file_path: str):
        """
        Converts json to yml file.
        """
        self.yml_converter.write(data=self.json_converter.read(source_file_path), file_path=destination_file_path)

    def to_xml(self, file_path: str):
        """
        Converts json to XML file.
        """
        pass