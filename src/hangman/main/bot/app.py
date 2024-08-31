from dishka import make_container
from dishka.integrations.telebot import setup_dishka
from telebot import TeleBot, custom_filters
from telebot.states.sync.middleware import StateMiddleware

from hangman.config import Config
from hangman.main.bot.ioc import (
    AdatersProvider,
    EnLocalizationProvider,
    InteractorProvider,
    RuLocalizationProvider,
)
from hangman.presentation.bot.handlers import register_handlers
from hangman.presentation.common.presenters import (
    InvalidConfigError,
)


def main():
    config = Config.load_config()
    match config.language:
        case "ru":
            localization_provider = RuLocalizationProvider()
        case "en":
            localization_provider = EnLocalizationProvider()
        case unsupported_language:
            raise InvalidConfigError(f"Unsupported language {unsupported_language}")

    if config.token is None:
        raise InvalidConfigError("No token specified for bot")

    bot = TeleBot(
        config.token,
        use_class_middlewares=True,
    )
    bot.add_custom_filter(custom_filters.StateFilter(bot))

    bot.setup_middleware(StateMiddleware(bot))

    register_handlers(bot)

    containter = make_container(
        localization_provider,
        AdatersProvider(),
        InteractorProvider(),
        context={Config: config},
    )
    setup_dishka(containter, bot)

    try:
        bot.infinity_polling()
    finally:
        containter.close()


if __name__ == "__main__":
    main()
