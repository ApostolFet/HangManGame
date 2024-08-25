from abc import ABC, abstractmethod
from dataclasses import dataclass

from hangman.application.dto import GameStep
from hangman.domain.entity import GameState


class InvalidConfigError(Exception): ...


@dataclass
class QuestionPlayAgain:
    question: str
    re_question: str
    positive_variants: set[str]
    negative_variants: set[str]


class Localization(ABC):
    def __init__(
        self,
        views_error: list[str],
        max_error: int,
    ):
        max_view_error = len(views_error)
        if max_view_error <= max_error:
            raise InvalidConfigError(
                f"The maximum number of errors is greater than possible ({max_view_error - 1}) "
            )

        self._views_error = views_error
        self._max_error = max_error

    @abstractmethod
    def get_question_play_again(self) -> QuestionPlayAgain: ...

    @abstractmethod
    def get_question_letter(self) -> str: ...

    @abstractmethod
    def get_view_greateing(self) -> str: ...

    @abstractmethod
    def get_view_game_step(self, game_step: GameStep) -> str: ...

    @abstractmethod
    def get_view_end_game(self, game_step: GameStep) -> str: ...

    @abstractmethod
    def get_view_goodbye(self) -> str: ...

    @abstractmethod
    def get_view_letter_error(self, letter: str) -> str: ...

    def _get_mask_word(self, word: str, guessed_indexes: set[int]) -> str:
        mask_list_letter = [
            letter if index in guessed_indexes else "*"
            for index, letter in enumerate(word)
        ]

        mask_word = "".join(mask_list_letter)
        return mask_word

    def _get_view_error(self, count_error: int) -> str:
        return self._views_error[-(self._max_error + 1) :][count_error]


class RuLocalization(Localization):
    def get_question_play_again(self) -> QuestionPlayAgain:
        return QuestionPlayAgain(
            question="Играть еще раз  (да/нет): ",
            re_question="Наберите один из ответов: да / нет                     ",
            positive_variants={"да"},
            negative_variants={"нет"},
        )

    def get_question_letter(self) -> str:
        return "Введите букву: "

    def get_view_greateing(self) -> str:
        return "Приветствую, Вас в ителлектуальной игре Висeлица"

    def get_view_goodbye(self):
        return "Спасибо за игру приходите еще"

    def get_view_game_step(self, game_step: GameStep) -> str:
        view_error = self._get_view_error(game_step.count_error)
        mask_word = self._get_mask_word(
            game_step.word, game_step.indeces_guessed_letters
        )
        try_letters = ", ".join(game_step.try_letters)

        return (
            view_error + f"\n\nСлово: {mask_word}; Использованные буквы: {try_letters};"
        )

    def get_view_letter_error(self, letter: str):
        print(f"Невалидный символ <{letter}> или уже использован", end="\r")

    def get_view_end_game(self, game_step: GameStep):
        match game_step.game_state:
            case GameState.VICTORY:
                return "Ура!!! Победа Ваша!!!"
            case GameState.DEFEAT:
                return f"Правильный ответ: {game_step.word}. Повезет в следующий раз"
            case _:
                raise Exception("Unexpected status")


class EnLocalization(Localization):
    def get_question_play_again(self) -> QuestionPlayAgain:
        return QuestionPlayAgain(
            question="Play again (yes/no): ",
            re_question="Type one of the following answers: yes / no",
            positive_variants={"yes"},
            negative_variants={"no"},
        )

    def get_question_letter(self) -> str:
        return "Enter a letter: "

    def get_view_greateing(self) -> str:
        return "Welcome to the intellectual game of Hangman."

    def get_view_goodbye(self) -> str:
        return "Thanks for the game, come again."

    def get_view_game_step(self, game_step: GameStep) -> str:
        view_error = self._get_view_error(game_step.count_error)
        mask_word = self._get_mask_word(
            game_step.word, game_step.indeces_guessed_letters
        )
        try_letters = ", ".join(game_step.try_letters)

        return view_error + f"\n\nWord: {mask_word}; Letters used: {try_letters};"

    def get_view_letter_error(self, letter: str) -> str:
        return f"Invalid <{letter}> character or already used"

    def get_view_end_game(self, game_step: GameStep):
        match game_step.game_state:
            case GameState.VICTORY:
                return "Yay!!! Victory is yours!!!"
            case GameState.DEFEAT:
                return f"The correct answer is {game_step.word}. Better luck next time"
            case _:
                raise Exception("Unexpected status")
