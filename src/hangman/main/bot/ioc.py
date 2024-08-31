from collections.abc import Iterator
from pathlib import Path
from sqlite3 import Connection, connect
from string import ascii_letters

from dishka import Provider, Scope, from_context, provide

from hangman.application.interactors import CreateGameInteractor, GuessLeterInteractor
from hangman.application.interfaces.letter_validator import LetterValidator
from hangman.application.interfaces.repo import HangManRepository
from hangman.application.interfaces.word_provider import WordProvider
from hangman.config import Config
from hangman.infrastructure.database.repo import SqliteHangManRepository
from hangman.infrastructure.letter_validator import (
    AlphabetLetterValidator,
    CompositeLetterValidator,
    LenLetterValidator,
)
from hangman.infrastructure.word_provider import FileWordProvider
from hangman.presentation.common.presenters import (
    EnglishPresenter,
    InvalidConfigError,
    Presenter,
    RussianPresenter,
)
from hangman.presentation.common.views_error import VIEW_ERRORS


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
    def get_presenters_provider(self, config: Config) -> Presenter:
        return RussianPresenter(views_error=VIEW_ERRORS, max_error=config.max_errors)


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
    def get_presenters_provider(self, config: Config) -> Presenter:
        return EnglishPresenter(views_error=VIEW_ERRORS, max_error=config.max_errors)


class AdatersProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_connection(self, config: Config) -> Iterator[Connection]:
        if config.db_path is None:
            raise InvalidConfigError("No db_path specified for sqlite")
        connection = connect(config.db_path)
        try:
            yield connection
        finally:
            connection.close()

    repo = provide(SqliteHangManRepository, provides=HangManRepository)


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
