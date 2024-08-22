from typing import Protocol

from hangman.application.dto import CreateHangMan, GameStep
from hangman.application.interactors import CreateGameInteractor, GuessLaterInteractor
from hangman.domain.entity import GameState
from hangman.domain.exception import LatterError


class Controller(Protocol):
    def get_letter(self) -> str: ...
    def get_play_again(self) -> bool: ...


class View(Protocol):
    def view_greating(self) -> None: ...
    def view_game_step(self, game: GameStep) -> None: ...
    def view_latter_error(self, latter: str): ...
    def view_end_game(self, game: GameStep) -> None: ...
    def view_goodbye(self) -> None: ...


class WordProvider(Protocol):
    def get_random_word(self) -> str: ...
    def _get_words(self) -> list[str]: ...


class Game:
    def __init__(
        self,
        controller: Controller,
        view: View,
        guess_later_interactor: GuessLaterInteractor,
        create_game_interactor: CreateGameInteractor,
        word_provider: WordProvider,
    ):
        self._controller = controller
        self._view = view
        self._guess_later_interactor = guess_later_interactor
        self._create_game_interactor = create_game_interactor
        self._word_provider = word_provider

    def launch(self):
        try:
            self._play()
        except KeyboardInterrupt:
            self._view.view_goodbye()

    def _play(self):
        self._view.view_greating()

        is_play_game = True
        while is_play_game:
            word = self._word_provider.get_random_word()
            self._start(word, 5)

            is_play_game = self._controller.get_play_again()

        self._view.view_goodbye()

    def _start(
        self,
        word: str,
        max_errors: int,
    ):
        game_step = self._create_game_interactor(
            1, CreateHangMan(word=word, max_error=max_errors)
        )
        self._view.view_game_step(game_step)
        while game_step.game_state == GameState.COMING:
            letter = self._controller.get_letter()
            try:
                game_step = self._guess_later_interactor(user_id=1, letter=letter)
            except LatterError as ex:
                self._view.view_latter_error(ex.latter)

            self._view.view_game_step(game_step)

        self._view.view_end_game(game_step)
