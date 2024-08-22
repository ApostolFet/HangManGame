import time

from hangman.adapters.cli.console import clear_line
from hangman.application.dto import GameStep
from hangman.domain.entity import GameState
from hangman.presentation.cli_game import View


class InvalidConfigError(Exception): ...


class CliView(View):
    def __init__(self, views_error: list[str], max_error: int):
        max_view_error = len(views_error)
        if max_view_error < max_error:
            raise InvalidConfigError(
                f"Максимальное число ошибок больше возможножного ({max_view_error}) "
            )

        self._views_error = views_error
        self._max_error = max_error

    def view_greating(self) -> None:
        print("Приветствую, Вас в ителектуальной игре Висeлица")
        time.sleep(3)
        print("\n" * 14, end="")

    def view_game_step(self, game: GameStep) -> None:
        view_error = self._get_view_error(game.count_error)
        mask_word = self._get_mask_word(game.word, game.indeces_guessed_letters)
        try_latters = ", ".join(game.try_letters)

        clear_line(14)
        print(
            view_error
            + f"\n\nСлово: {mask_word}; Использованные буквы: {try_latters};",
            end="\n",
        )

    def view_end_game(self, game: GameStep) -> None:
        clear_line(4)
        print("\n")
        match game.game_state:
            case GameState.VICTORY:
                print("Ура!!! Победа Ваша!!!")
            case GameState.DEFEAT:
                print(f"Правильный ответ: {game.word}. Повезет в следующий раз")
            case _:
                raise Exception("Неожиданный статус")

    def view_goodbye(self):
        print("\nСпасибо за игру приходите еще")

    def view_latter_error(self, latter: str):
        print(f"Невалидный символ <{latter}> или уже использован", end="\r")

    def _get_mask_word(self, word: str, guessed_indexes: set[int]) -> str:
        mask_list_latter = [
            latter if index in guessed_indexes else "*"
            for index, latter in enumerate(word)
        ]

        mask_word = "".join(mask_list_latter)
        return mask_word

    def _get_view_error(self, count_error: int) -> str:
        return self._views_error[-(self._max_error + 1) :][count_error]
