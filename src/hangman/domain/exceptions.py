class LetterError(Exception):
    def __init__(
        self,
        *args,
        letter: str,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.letter = letter


class LetterAlredyGuessError(LetterError): ...


class LetterInvalidError(LetterError): ...
