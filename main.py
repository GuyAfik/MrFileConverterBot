from dependency_injector.wiring import Provide, inject
from telegram.ext import Updater

import mr_file_converter.dispatcher as dp
from mr_file_converter.containers import Application


@inject
def main(
    updater: Updater = Provide[Application.core.updater]
):
    dispatcher = updater.dispatcher
    dp.setup_dispatcher(dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    application = Application()
    application.core.init_resources()
    application.wire(modules=[__name__, "mr_file_converter.dispatcher"])

    main()
