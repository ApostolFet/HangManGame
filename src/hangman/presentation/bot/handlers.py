from threading import local
from dishka.integrations.telebot import FromDishka, inject
from telebot import TeleBot, types
from telebot.states.sync.context import StateContext

from hangman.application.interactors import CreateGameInteractor, GuessLeterInteractor
from hangman.domain.entity import GameState
from hangman.domain.exceptions import LetterError
from hangman.presentation.core.localizations import Localization
from hangman.presentation.bot.states import GameStates


@inject
def start_game(
    message: types.Message,
    bot: TeleBot,
    state: StateContext,
    localization: FromDishka[Localization],
    create_game_interactor: FromDishka[CreateGameInteractor],
):
    bot.send_message(message.chat.id, localization.get_view_greateing())
    game_step = create_game_interactor(message.chat.id)
    bot.send_message(message.chat.id, localization.get_view_game_step(game_step))

    state.set(GameStates.playing)


@inject
def guess_letter(
    message: types.Message,
    bot: TeleBot,
    state: StateContext,
    localization: FromDishka[Localization],
    guess_interactor: FromDishka[GuessLeterInteractor],
):
    user_id = message.chat.id
    letter = message.text

    if letter is None:
        bot.send_message(user_id, localization.get_view_letter_error(""))
        return

    try:
        game_step = guess_interactor(user_id, letter)
    except LetterError as ex:
        bot.send_message(user_id, localization.get_view_letter_error(ex.letter))
        return

    view_game_step = localization.get_view_game_step(game_step)
    bot.send_message(user_id, view_game_step)

    if game_step.game_state is GameState.COMING:
        return

    view_end_game = localization.get_view_end_game(game_step)
    bot.send_message(user_id, view_end_game)
    state.delete()


@inject
def end_game(
    message: types.Message,
    bot: TeleBot,
    state: StateContext,
    localization: FromDishka[Localization],
):
    bot.send_message(message.chat.id, localization.get_view_goodbye())
    state.delete()


def register_handlers(bot: TeleBot):
    bot.register_message_handler(start_game, commands=["start"], pass_bot=True)
    bot.register_message_handler(
        guess_letter,
        func=lambda message: message.text != "",
        pass_bot=True,
        state=GameStates.playing,
    )
    bot.register_message_handler(
        end_game,
        commands=["end"],
        state=GameStates.playing,
        pass_bot=True,
    )
