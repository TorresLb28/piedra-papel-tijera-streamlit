"""Rock, Paper, Scissors game logic."""

import random

VALID_MOVES: tuple[str, ...] = ("piedra", "papel", "tijera")

_BEATS: dict[str, str] = {
    "piedra": "tijera",
    "papel": "piedra",
    "tijera": "papel",
}


def _validate_move(move: str, argument_name: str) -> None:
    """Validate that a move is one of the supported options.

    Args:
        move: Move value to validate.
        argument_name: Parameter name used in the error message.

    Raises:
        ValueError: If the move is not exactly one of the valid options.
    """
    if move not in VALID_MOVES:
        raise ValueError(
            f"{argument_name} must be one of {VALID_MOVES}, received {move!r}"
        )


def determine_winner(player_move: str, computer_move: str) -> str:
    """Determine the outcome of a round.

    Args:
        player_move: Player's move, in lowercase.
        computer_move: Computer's move, in lowercase.

    Returns:
        ``"player"`` if the player wins, ``"computer"`` if the computer
        wins, or ``"tie"`` if both moves are equal.

    Raises:
        ValueError: If either move is not exactly ``piedra``, ``papel`` or
            ``tijera``.
    """
    _validate_move(player_move, "player_move")
    _validate_move(computer_move, "computer_move")

    if player_move == computer_move:
        return "tie"
    if _BEATS[player_move] == computer_move:
        return "player"
    return "computer"


def get_computer_move() -> str:
    """Return a random move for the computer.

    Returns:
        One of ``piedra``, ``papel`` or ``tijera``.
    """
    return random.choice(VALID_MOVES)
