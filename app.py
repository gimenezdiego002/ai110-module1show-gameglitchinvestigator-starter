import os
import random
import streamlit as st
# FIX (Bug #12): Game logic refactored into logic_utils.py using Claude Code agent
# mode; app.py now only handles the UI and imports the logic from there.
from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

# FIX (Bug #7): Debug info reveals the secret, so it is only shown when the
# developer starts the app with GAME_DEBUG=1. The AI and I chose an environment
# variable over a checkbox because a player could just tick a checkbox.
DEBUG_MODE = os.environ.get("GAME_DEBUG") == "1"


# FIX (Bug #1): New Game used to reset only attempts and the secret, never the
# status, so "You already won" blocked replays. The AI helped gather every reset
# into one function that New Game and difficulty changes both use.
def start_new_game(difficulty: str):
    low, high = get_range_for_difficulty(difficulty)
    st.session_state.secret = random.randint(low, high)  # FIX: was always 1-100
    st.session_state.attempts = 0  # FIX (Bug #2): started at 1, so Normal showed 7 left
    st.session_state.score = 0
    st.session_state.status = "playing"  # FIX (Bug #1): the missing reset
    st.session_state.history = []
    st.session_state.difficulty = difficulty
    st.session_state.game_id = st.session_state.get("game_id", 0) + 1  # FIX: clears the guess box


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("Guess the secret number before you run out of attempts.")

# FIX (Bug #8): Difficulty moved from the collapsible sidebar to the main page.
difficulty = st.radio(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
    horizontal=True,
)

attempt_limit = get_attempt_limit(difficulty)
low, high = get_range_for_difficulty(difficulty)

st.caption(f"Range: {low} to {high} · Attempts allowed: {attempt_limit}")

# FIX (Bug #8): changing difficulty used to keep the old secret (e.g. 87 on Easy)
if st.session_state.get("difficulty") != difficulty:
    start_new_game(difficulty)

st.subheader("Make a guess")

# FIX (Bug #3): "Attempts left" was drawn before the guess was counted, so it lagged
# one click behind. The AI suggested reserving this spot and filling it in later.
status_box = st.container()

raw_guess = st.text_input(
    f"Enter your guess ({low} to {high}):",
    key=f"guess_input_{st.session_state.game_id}",
)

playing = st.session_state.status == "playing"

col1, col2, col3 = st.columns(3)
with col1:
    # FIX (Bug #1): replaces the old st.stop(); Submit is disabled once the game ends
    submit = st.button("Submit Guess 🚀", disabled=not playing)
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_game(difficulty)
    st.rerun()

if submit and playing:
    # FIX (Bug #9): pass the difficulty's range so out-of-range guesses are rejected
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.error(err)
    else:
        # FIX (Bug #4): only count valid guesses (invalid input used to cost an attempt)
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX (Bug #6): the secret was turned into text on even attempts; now always an int
        outcome, message = check_guess(guess_int, st.session_state.secret)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
        else:
            if show_hint:
                st.warning(message)
            else:
                # FIX: with hints off, a wrong guess used to show nothing at all
                st.warning("❌ Not quite. Try again!")

            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"

# FIX (Bug #1): the win/lose message now stays until New Game is clicked
with status_box:
    if st.session_state.status == "won":
        st.success(
            f"🎉 You won in {st.session_state.attempts} guess(es)! "
            f"The secret was {st.session_state.secret}. "
            f"Final score: {st.session_state.score}. "
            f"Click New Game to play again."
        )
    elif st.session_state.status == "lost":
        st.error(
            f"Out of attempts! "
            f"The secret was {st.session_state.secret}. "
            f"Score: {st.session_state.score}. "
            f"Click New Game to try again."
        )
    else:
        st.info(
            f"Guess a number between {low} and {high}. "
            f"Attempts left: {attempt_limit - st.session_state.attempts}"
        )

if DEBUG_MODE:
    with st.expander("Developer Debug Info"):
        st.write("Secret:", st.session_state.secret)
        st.write("Attempts:", st.session_state.attempts)
        st.write("Score:", st.session_state.score)
        st.write("Difficulty:", difficulty)
        st.write("History:", st.session_state.history)

st.divider()
st.caption("Codepath AI 110 ·  Game Glitch Investigator")
