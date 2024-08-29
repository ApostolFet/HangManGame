from dishka.integrations.telebot import FromDishka, inject
from telebot import TeleBot, types
from telebot.states.sync.context import StateContext

from hangman.application.interactors import CreateGameInteractor, GuessLeterInteractor
from hangman.domain.entity import GameState
from hangman.domain.exceptions import LetterError
from hangman.presentation.bot.states import GameStates
from hangman.presentation.common.presenters import Presenter


@inject
def start_game(
    message: types.Message,
    bot: TeleBot,
    state: StateContext,
    presenter: FromDishka[Presenter],
    create_game_interactor: FromDishka[CreateGameInteractor],
):
    bot.send_message(message.chat.id, presenter.get_view_greateing())
    game_step = create_game_interactor(message.chat.id)
    view_game_step = presenter.get_view_game_step(game_step)
    message_sended = bot.send_message(
        message.chat.id,
        f"```hangman\n{view_game_step}\n```",
        parse_mode="Markdown",
    )

    state.set(GameStates.playing)
    state.add_data(game_step_message_id=message_sended.id)


@inject
def guess_letter(
    message: types.Message,
    bot: TeleBot,
    state: StateContext,
    presenter: FromDishka[Presenter],
    guess_interactor: FromDishka[GuessLeterInteractor],
):
    user_id = message.chat.id
    letter = message.text

    bot.delete_message(user_id, message.id)

    with state.data() as data:
        delete_message = data.get("delete_message")
    if delete_message:
        bot.delete_message(user_id, delete_message)
        state.add_data(delete_message=None)

    if letter is None:
        message_sended = bot.send_message(user_id, presenter.get_view_letter_error(""))
        state.add_data(delete_message=message_sended.id)
        return

    try:
        game_step = guess_interactor(user_id, letter)
    except LetterError as ex:
        message_sended = bot.send_message(
            user_id, presenter.get_view_letter_error(ex.letter)
        )
        state.add_data(delete_message=message_sended.id)
        return

    view_game_step = presenter.get_view_game_step(game_step)
    view_hangman = presenter.get_view_hangman(game_step)
    question_letter = presenter.get_question_letter()
    telegram_view_game_step = f"```hangman\n{view_game_step}\n```\n{question_letter}"

    with state.data() as data:
        game_step_message_id = data.get("game_step_message_id")

    if game_step_message_id:
        bot.edit_message_text(
            telegram_view_game_step,
            user_id,
            game_step_message_id,
            parse_mode="Markdown",
        )
    else:
        message_sended = bot.send_message(
            user_id,
            f"```hangman\n{view_hangman}\n```\n{view_game_step}\n{question_letter}",
            parse_mode="Markdown",
        )
        state.add_data(game_step_message_id=message_sended.id)

    if game_step.game_state is GameState.COMING:
        return

    view_end_game = presenter.get_view_end_game(game_step)

    bot.send_message(user_id, view_end_game)
    state.delete()


@inject
def end_game(
    message: types.Message,
    bot: TeleBot,
    state: StateContext,
    presenter: FromDishka[Presenter],
):
    bot.send_message(message.chat.id, presenter.get_view_goodbye())
    state.delete()


def register_handlers(bot: TeleBot):
    bot.register_message_handler(start_game, commands=["start"], pass_bot=True)
    bot.register_message_handler(
        end_game,
        commands=["end"],
        state=GameStates.playing,
        pass_bot=True,
    )
    bot.register_message_handler(
        guess_letter,
        func=lambda message: message.text != "",
        pass_bot=True,
        state=GameStates.playing,
    )
