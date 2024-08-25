from abc import abstractmethod
from typing import Protocol


class LetterValidator(Protocol):
    @abstractmethod
    def validate(self, letter: str):
        """Validate letter and raise LetterInvalidError if latter invalid"""
        ...
