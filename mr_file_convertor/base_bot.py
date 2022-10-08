import os
from abc import ABC, abstractmethod


class BaseBot(ABC):
    def __init__(self, token: str):
        self.token = token or os.getenv('BOT_TOKEN')

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def help_command(self):
        pass
