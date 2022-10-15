from abc import ABC, abstractmethod
from typing import Any


class BaseConverter(ABC):

    @abstractmethod
    def read(self, file_path: str, **kwargs):
        pass

    @abstractmethod
    def write(self, data: Any, file_path: str):
        pass
