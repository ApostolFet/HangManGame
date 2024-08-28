from typing import Protocol

from hangman.application.dto import GameStep
from hangman.application.interactors import CreateGameInteractor, GuessLeterInteractor
from hangman.domain.entity import GameState
from hangman.domain.exceptions import LetterError


class Controller(Protocol):
    def get_letter(self) -> str: ...
    def get_play_again(self) -> bool: ...
    def view_greating(self) -> None: ...
    def view_game_step(self, game: GameStep) -> None: ...
    def view_letter_error(self, letter: str): ...
    def view_end_game(self, game: GameStep) -> None: ...
    def view_goodbye(self) -> None: ...


class Game:
    def __init__(
        self,
        controller: Controller,
        guess_later_interactor: GuessLeterInteractor,
        create_game_interactor: CreateGameInteractor,
    ):
        self._controller = controller
        self._guess_later_interactor = guess_later_interactor
        self._create_game_interactor = create_game_interactor

    def launch(self):
        try:
            self._play()
        except KeyboardInterrupt:
            self._controller.view_goodbye()

    def _play(self):
        self._controller.view_greating()

        is_play_game = True
        while is_play_game:
            self._start()

            is_play_game = self._controller.get_play_again()

        self._controller.view_goodbye()

    def _start(self):
        game_step = self._create_game_interactor(1)
        self._controller.view_game_step(game_step)

        while game_step.game_state == GameState.COMING:
            letter = self._controller.get_letter()
            try:
                game_step = self._guess_later_interactor(user_id=1, letter=letter)
            except LetterError as ex:
                self._controller.view_letter_error(ex.letter)
                continue

            self._controller.view_game_step(game_step)

        self._controller.view_end_game(game_step)
