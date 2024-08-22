class LatterError(Exception):
    def __init__(
        self,
        *args,
        latter: str,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.latter = latter


class LatterAlredyGuessError(LatterError): ...


class LatterInvalidError(LatterError): ...
