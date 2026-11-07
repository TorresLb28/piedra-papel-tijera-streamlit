import pytest

from game_logic import determine_winner


@pytest.mark.parametrize(
    ("player_move", "computer_move"),
    [
        ("piedra", "tijera"),
        ("papel", "piedra"),
        ("tijera", "papel"),
    ],
)
def test_player_wins(player_move: str, computer_move: str) -> None:
    assert determine_winner(player_move, computer_move) == "player"


@pytest.mark.parametrize(
    ("player_move", "computer_move"),
    [
        ("piedra", "papel"),
        ("papel", "tijera"),
        ("tijera", "piedra"),
    ],
)
def test_computer_wins(player_move: str, computer_move: str) -> None:
    assert determine_winner(player_move, computer_move) == "computer"


@pytest.mark.parametrize(
    ("player_move", "computer_move"),
    [
        ("piedra", "piedra"),
        ("papel", "papel"),
        ("tijera", "tijera"),
    ],
)
def test_tie(player_move: str, computer_move: str) -> None:
    assert determine_winner(player_move, computer_move) == "tie"


@pytest.mark.parametrize(
    ("player_move", "computer_move"),
    [
        ("lagarto", "piedra"),
        ("piedra", "lagarto"),
        ("", "tijera"),
        ("Piedra", "tijera"),
    ],
)
def test_invalid_moves_raise_value_error(player_move: str, computer_move: str) -> None:
    with pytest.raises(ValueError):
        determine_winner(player_move, computer_move)
