import os

from dependency_injector import containers, providers
from telegram.ext import Updater


class Core(containers.DeclarativeContainer):

    updater = providers.Resource(
        Updater,
        token=os.getenv('BOT_TOKEN'),
    )


class Services(containers.DeclarativeContainer):
    pass
