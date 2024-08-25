import time

from hangman.application.dto import GameStep
from hangman.presentation.cli.console import clear_line
from hangman.presentation.cli.game import Controller
from hangman.presentation.core.localizations import Localization


class CliController(Controller):
    def __init__(self, localization: Localization):
        self._localization = localization
        self._window_heigh = 14

    def get_letter(self) -> str:
        return input(self._localization.get_question_letter())

    def get_play_again(self) -> bool:
        print()

        question = self._localization.get_question_play_again()
        user_input = input(question.question)

        if user_input.strip().lower() in question.positive_variants:
            return True
        elif user_input.strip().lower() in question.negative_variants:
            return False
        else:
            print(question.re_question + "                     ")
            return self.get_play_again()

    def view_greating(self) -> None:
        print(self._localization.get_view_greateing())
        time.sleep(1)
        print("\n" * self._window_heigh, end="")

    def view_game_step(self, game: GameStep) -> None:
        clear_line(self._window_heigh)
        print(
            self._localization.get_view_game_step(game),
            end="\n",
        )

    def view_end_game(self, game: GameStep) -> None:
        clear_line(4)
        print("\n")
        print(self._localization.get_view_end_game(game))

    def view_goodbye(self):
        print("\n" + self._localization.get_view_goodbye())

    def view_letter_error(self, letter: str):
        print(self._localization.get_view_letter_error(letter), end="\r")
