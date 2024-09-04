import pytest
from hangman.domain.entity import GameState, HangManGame
from hangman.domain.exceptions import LetterAlredyGuessError


def test_hangman_guess_letter() -> None:
    expected_indeces_guessed_letters = {0, 3}

    game = HangManGame(
        word="test",
        max_error=5,
    )
    result_guess = game.guess("t")
    result_indeces_guessed_letters = game.indeces_guessed_letters

    assert result_guess
    assert result_indeces_guessed_letters == expected_indeces_guessed_letters


def test_hangman_not_guess_letter() -> None:
    game = HangManGame(
        word="test",
        max_error=5,
    )

    result_guess = game.guess("d")
    result_indeces_guessed_letters = game.indeces_guessed_letters

    assert not result_guess
    assert not result_indeces_guessed_letters


def test_hangman_used_letters() -> None:
    expected_used_letter = ["t", "e", "q"]

    game = HangManGame(
        word="test",
        max_error=5,
    )
    for letter in expected_used_letter:
        game.guess(letter)
    result_used_letter = game.used_letters

    assert expected_used_letter == result_used_letter


def test_hangman_letter_already_guess() -> None:
    game = HangManGame(
        word="test",
        max_error=5,
    )
    game.guess("t")

    with pytest.raises(LetterAlredyGuessError):
        game.guess("t")


def test_hangman_count_error() -> None:
    expected_count_error = 3

    game = HangManGame(
        word="test",
        max_error=expected_count_error + 1,
    )
    game.guess("w")
    game.guess("r")
    game.guess("o")
    result_count_error = game.count_error

    assert expected_count_error == result_count_error


def test_hangman_word() -> None:
    expected_word = "test"

    game = HangManGame(
        word=expected_word,
        max_error=5,
    )
    result_word = game.word

    assert expected_word == result_word


def test_hangman_win_game() -> None:
    game = HangManGame(
        word="test",
        max_error=5,
    )

    game.guess("t")
    game.guess("e")
    game.guess("s")

    assert game.game_state is GameState.VICTORY


def test_hangman_defeat_game() -> None:
    game = HangManGame(
        word="test",
        max_error=5,
    )

    game.guess("w")
    game.guess("r")
    game.guess("o")
    game.guess("n")
    game.guess("g")

    assert game.game_state is GameState.DEFEAT


def test_hangman_comming_game() -> None:
    expected_game_states = [GameState.COMING, GameState.COMING, GameState.COMING]

    result_game_states = []
    game = HangManGame(
        word="test",
        max_error=5,
    )
    result_game_states.append(game.game_state)
    game.guess("t")
    result_game_states.append(game.game_state)
    game.guess("w")
    result_game_states.append(game.game_state)

    assert expected_game_states == result_game_states


def test_hangman_cant_guess_two_more_letter() -> None:
    game = HangManGame(
        word="test",
        max_error=5,
    )
    assert not game.guess("te")


def test_hangman_guess_case_sensitivity() -> None:
    game = HangManGame(
        word="test",
        max_error=5,
    )

    upper_case_result = game.guess("T")
    lower_case_result = game.guess("e")

    assert all((upper_case_result, lower_case_result))
    with pytest.raises(LetterAlredyGuessError):
        game.guess("t")


@pytest.mark.parametrize(
    "guess_letters",
    [
        ("t", "e", "d"),
        ("e", "d", "t"),
        ("d", "e", "t"),
        ("p", "e", "s", "t"),
        ("d", "a", "y", "s"),
        ("q", "d", "p"),
    ],
)
def test_hangman_save_order_used_letters(guess_letters: tuple[str]) -> None:
    game = HangManGame(
        word="test",
        max_error=5,
    )
    expected_used_letters = "".join(guess_letters)

    for letter in guess_letters:
        game.guess(letter)

    result = "".join(game.used_letters)

    assert result == expected_used_letters
