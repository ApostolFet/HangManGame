from pathlib import Path
from string import ascii_letters

from hangman.application.interactors import (
    CreateGameInteractor,
    GuessLeterInteractor,
)
from hangman.config import Config
from hangman.infrastructure.letter_validator import (
    AlphabetLetterValidator,
    CompositeLetterValidator,
    LenLetterValidator,
)
from hangman.infrastructure.repo import InMemoryHangmanRepository
from hangman.infrastructure.word_provider import FileWordProvider
from hangman.presentation.cli.game import Game
from hangman.presentation.cli.view import ConsoleView
from hangman.presentation.common.presenters import (
    EnglishPresenter,
    InvalidConfigError,
    Presenter,
    RussianPresenter,
)
from hangman.presentation.common.views_error import VIEW_ERRORS


def main() -> None:
    config = Config.load_config()

    match config.language:
        case "ru":
            word_provider = FileWordProvider(Path("files/ru_words.txt"))
            presenter: Presenter = RussianPresenter(
                max_error=config.max_errors,
                views_error=VIEW_ERRORS,
            )
            alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"

        case "en":
            word_provider = FileWordProvider(Path("files/en_words.txt"))
            presenter = EnglishPresenter(
                max_error=config.max_errors,
                views_error=VIEW_ERRORS,
            )

            alphabet = ascii_letters
        case unsupported_language:
            raise InvalidConfigError(f"Unsupported language {unsupported_language}")

    repo = InMemoryHangmanRepository()
    view = ConsoleView(presenter)

    letter_validator = CompositeLetterValidator(
        (LenLetterValidator(), AlphabetLetterValidator(alphabet)),
    )

    game = Game(
        view=view,
        guess_later_interactor=GuessLeterInteractor(repo, letter_validator),
        create_game_interactor=CreateGameInteractor(
            repo,
            word_provider,
            config.max_errors,
        ),
    )
    game.launch()


if __name__ == "__main__":
    main()
