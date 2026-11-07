"""Streamlit interface for the Rock, Paper, Scissors game."""

import streamlit as st

from game_logic import VALID_MOVES, determine_winner, get_computer_move

PLAYER_MOVE_KEY = "player_move"
PLAYER_WINS_KEY = "player_wins"
COMPUTER_WINS_KEY = "computer_wins"
TIES_KEY = "ties"
LAST_ROUND_KEY = "last_round"

RESULT_MESSAGES: dict[str, str] = {
    "player": "Ganaste la ronda.",
    "computer": "La computadora ganó la ronda.",
    "tie": "Empate.",
}


def _initialize_session_state() -> None:
    """Initialize the scoreboard and last round state exactly once."""
    defaults = {
        PLAYER_WINS_KEY: 0,
        COMPUTER_WINS_KEY: 0,
        TIES_KEY: 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _reset_scoreboard() -> None:
    """Set every score to zero and clear the last round result."""
    st.session_state[PLAYER_WINS_KEY] = 0
    st.session_state[COMPUTER_WINS_KEY] = 0
    st.session_state[TIES_KEY] = 0
    st.session_state.pop(LAST_ROUND_KEY, None)


def _play_round() -> None:
    """Resolve a round, update the scoreboard and store its result."""
    player_move = st.session_state.get(PLAYER_MOVE_KEY, VALID_MOVES[0])
    computer_move = get_computer_move()
    result = determine_winner(player_move, computer_move)

    if result == "player":
        st.session_state[PLAYER_WINS_KEY] += 1
    elif result == "computer":
        st.session_state[COMPUTER_WINS_KEY] += 1
    else:
        st.session_state[TIES_KEY] += 1

    st.session_state[LAST_ROUND_KEY] = {
        "player_move": player_move,
        "computer_move": computer_move,
        "result": result,
    }


def _format_move(move: str) -> str:
    """Return a capitalized label for a move."""
    return move.capitalize()


def _render_scoreboard() -> None:
    """Render the persistent scoreboard."""
    st.subheader("Marcador")
    player_column, computer_column, ties_column = st.columns(3)
    player_column.metric("Jugador", st.session_state[PLAYER_WINS_KEY])
    computer_column.metric("Computadora", st.session_state[COMPUTER_WINS_KEY])
    ties_column.metric("Empates", st.session_state[TIES_KEY])


def _render_last_round() -> None:
    """Render the moves and outcome of the most recent round."""
    last_round = st.session_state.get(LAST_ROUND_KEY)
    if not isinstance(last_round, dict):
        st.info("Selecciona una jugada y pulsa «Jugar» para comenzar.")
        return

    st.subheader("Última ronda")
    st.write(f"**Tu jugada:** {_format_move(last_round['player_move'])}")
    st.write(
        f"**Jugada de la computadora:** {_format_move(last_round['computer_move'])}"
    )

    result = last_round["result"]
    if result == "player":
        st.success(RESULT_MESSAGES[result])
    elif result == "computer":
        st.error(RESULT_MESSAGES[result])
    else:
        st.info(RESULT_MESSAGES[result])


def main() -> None:
    """Run the Streamlit application."""
    st.set_page_config(
        page_title="Piedra, Papel o Tijera",
        layout="centered",
    )
    _initialize_session_state()

    st.title("Piedra, Papel o Tijera")
    st.caption("Juega contra la computadora y lleva el marcador de tus rondas.")

    _render_scoreboard()

    st.selectbox(
        "Elige tu jugada",
        options=VALID_MOVES,
        format_func=_format_move,
        key=PLAYER_MOVE_KEY,
    )

    play_column, reset_column = st.columns(2)
    play_column.button(
        "Jugar",
        type="primary",
        use_container_width=True,
        on_click=_play_round,
    )
    reset_column.button(
        "Reiniciar marcador",
        use_container_width=True,
        on_click=_reset_scoreboard,
    )

    _render_last_round()


if __name__ == "__main__":
    main()
