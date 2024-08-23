from pathlib import Path

from hangman.adapters.repo import InMemoryHangmanRepository
from hangman.adapters.word_provider import FileWordProvider
from hangman.application.interactors import CreateGameInteractor, GuessLaterInteractor
from hangman.config import Config
from hangman.presentation.cli.controller import CliController
from hangman.presentation.cli.game import Game
from hangman.presentation.cli.views_error import VIEW_ERRORS
from hangman.presentation.core.localizations import EnLocalization, RuLocalization


def main():
    config = Config.load_config()

    match config.language:
        case "ru":
            word_provider = FileWordProvider(Path("files/ru_words.txt"))
            localization = RuLocalization(
                max_error=config.max_errors, views_error=VIEW_ERRORS
            )
        case "en":
            word_provider = FileWordProvider(Path("files/en_words.txt"))
            localization = EnLocalization(
                max_error=config.max_errors, views_error=VIEW_ERRORS
            )

    repo = InMemoryHangmanRepository()
    controler = CliController(localization)

    game = Game(
        controller=controler,
        guess_later_interactor=GuessLaterInteractor(repo),
        create_game_interactor=CreateGameInteractor(repo),
        word_provider=word_provider,
        max_errors=config.max_errors,
    )
    game.launch()


if __name__ == "__main__":
    main()
