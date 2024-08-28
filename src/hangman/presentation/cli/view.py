import time

from hangman.application.dto import GameStep
from hangman.presentation.cli.console import clear, clear_line
from hangman.presentation.cli.game import View
from hangman.presentation.common.presenters import Presenter


class ConsoleView(View):
    def __init__(self, presenter: Presenter):
        self._presenter = presenter

    def get_letter(self) -> str:
        return input(self._presenter.get_question_letter())

    def get_play_again(self) -> bool:
        print()

        question = self._presenter.get_question_play_again()
        user_input = input(question.question)

        if user_input.strip().lower() in question.positive_variants:
            return True
        elif user_input.strip().lower() in question.negative_variants:
            return False
        else:
            print(question.re_question + "                     ")
            return self.get_play_again()

    def view_greating(self) -> None:
        print(self._presenter.get_view_greateing())
        time.sleep(2)

    def view_game_step(self, game: GameStep) -> None:
        clear()
        print(
            self._presenter.get_view_game_step(game),
            end="\n",
        )

    def view_end_game(self, game: GameStep) -> None:
        print("\n")
        print(self._presenter.get_view_end_game(game))

    def view_goodbye(self):
        print("\n")
        print(self._presenter.get_view_goodbye())

    def view_letter_error(self, letter: str):
        print(self._presenter.get_view_letter_error(letter), end="\r")
        clear_line(1)
