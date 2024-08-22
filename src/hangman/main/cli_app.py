from pathlib import Path

from hangman.adapters.cli.controller import CliController
from hangman.adapters.cli.view import CliView
from hangman.adapters.cli.views_error import VIEW_ERRORS
from hangman.adapters.repo import InMemoryHangmanRepository
from hangman.adapters.word_provider import FileWordProvider
from hangman.application.interactors import CreateGameInteractor, GuessLaterInteractor
from hangman.presentation.cli_game import Game


def main():
    repo = InMemoryHangmanRepository()
    controler = CliController()
    view = CliView(max_error=5, views_error=VIEW_ERRORS)
    word_provider = FileWordProvider(Path("files/words.txt"))
    game = Game(
        controller=controler,
        view=view,
        guess_later_interactor=GuessLaterInteractor(repo),
        create_game_interactor=CreateGameInteractor(repo),
        word_provider=word_provider,
    )
    game.launch()


if __name__ == "__main__":
    main()
