class LetterError(Exception):
    def __init__(
        self,
        *args: object,
        letter: str,
    ):
        super().__init__(*args)
        self.letter = letter


class LetterAlredyGuessError(LetterError): ...


class LetterInvalidError(LetterError): ...
