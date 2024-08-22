from hangman.presentation.cli_game import Controller


class CliController(Controller):
    def get_letter(self) -> str:
        return input("Введите букву: ")

    def get_play_again(self) -> bool:
        print()
        user_input = input("Играть еще раз  (да/нет): ")

        if user_input.strip().lower() == "да":
            return True
        elif user_input.strip().lower() == "нет":
            return False
        else:
            print("Наберите один из ответов: да / нет                     ")
            return self.get_play_again()
