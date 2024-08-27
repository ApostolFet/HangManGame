from pathlib import Path
from string import ascii_letters

import telebot
from dishka import Provider, Scope, from_context, make_container, provide
from dishka.integrations.telebot import setup_dishka
from telebot import custom_filters
from telebot.states.sync.middleware import StateMiddleware

from hangman.application.interactors import CreateGameInteractor, GuessLeterInteractor
from hangman.application.interfaces.letter_validator import LetterValidator
from hangman.application.interfaces.repo import HangManRepository
from hangman.application.interfaces.word_provider import WordProvider
from hangman.config import Config
from hangman.infrastructure.letter_validator import (
    AlphabetLetterValidator,
    CompositeLetterValidator,
    LenLetterValidator,
)
from hangman.infrastructure.repo import InMemoryHangmanRepository
from hangman.infrastructure.word_provider import FileWordProvider
from hangman.presentation.bot.handlers import register_handlers
from hangman.presentation.cli.views_error import VIEW_ERRORS
from hangman.presentation.core.localizations import (
    EnLocalization,
    InvalidConfigError,
    Localization,
    RuLocalization,
)


class RuLocalizationProvider(Provider):
    scope = Scope.APP
    config = from_context(Config)

    @provide
    def get_word_provider(self) -> WordProvider:
        return FileWordProvider(Path("files/ru_words.txt"))

    @provide
    def get_letter_validator(self) -> LetterValidator:
        alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

        letter_validator = CompositeLetterValidator(
            (LenLetterValidator(), AlphabetLetterValidator(alphabet)),
        )
        return letter_validator

    @provide
    def get_localization_provider(self, config: Config) -> Localization:
        return RuLocalization(views_error=VIEW_ERRORS, max_error=config.max_errors)


class EnLocalizationProvider(Provider):
    scope = Scope.APP

    config = from_context(Config)

    @provide
    def get_word_provider(self) -> WordProvider:
        return FileWordProvider(Path("files/en_words.txt"))

    @provide
    def get_letter_validator(self) -> LetterValidator:
        letter_validator = CompositeLetterValidator(
            (LenLetterValidator(), AlphabetLetterValidator(ascii_letters)),
        )
        return letter_validator

    @provide
    def get_localization_provider(self, config: Config) -> Localization:
        return EnLocalization(views_error=VIEW_ERRORS, max_error=config.max_errors)


class AdatersProvider(Provider):
    scope = Scope.APP
    repo = provide(InMemoryHangmanRepository, provides=HangManRepository)


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    hangman_interactors = provide(GuessLeterInteractor)

    @provide
    def get_create_game_interactor(
        self,
        repo: HangManRepository,
        word_provider: WordProvider,
        config: Config,
    ) -> CreateGameInteractor:
        return CreateGameInteractor(repo, word_provider, config.max_errors)


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

    bot = telebot.TeleBot(
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
