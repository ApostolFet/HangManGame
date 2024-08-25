from collections.abc import Iterable

from hangman.application.interfaces.letter_validator import LetterValidator
from hangman.domain.exception import LetterInvalidError


class LenLetterValidator(LetterValidator):
    def validate(self, letter: str):
        if len(letter) != 1:
            raise LetterInvalidError("Letter must be length equal one", letter=letter)


class AlphabetLetterValidator(LetterValidator):
    def __init__(self, alphabet: Iterable[str]):
        self._alphabet = set(map(str.lower, alphabet))

    def validate(self, letter: str):
        if letter.lower() not in self._alphabet:
            raise LetterInvalidError("Letter not in alphabet", letter=letter)


class CompositeLetterValidator(LetterValidator):
    def __init__(self, validators: Iterable[LetterValidator]):
        self._validators = validators

    def validate(self, letter: str):
        for validator in self._validators:
            validator.validate(letter)
