from telebot.states import State, StatesGroup


class GameStates(StatesGroup):
    playing = State()
