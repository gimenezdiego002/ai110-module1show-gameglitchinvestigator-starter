# FIX (Bug #8): Refactored from app.py with Claude Code agent mode; Hard was 1-50
# (easier than Normal), so the AI and I reordered ranges to get harder each level.
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50  # FIX: was 1-100
    if difficulty == "Hard":
        return 1, 100  # FIX: was 1-50
    return 1, 100


# FIX (Bug #8): Moved the attempt map out of app.py with the AI; Easy had fewer
# attempts (6) than Normal (8). Hard gets 7, the minimum to always solve 1-100.
def get_attempt_limit(difficulty: str):
    """Return how many guesses the player gets for a given difficulty."""
    if difficulty == "Easy":
        return 10
    if difficulty == "Normal":
        return 8
    if difficulty == "Hard":
        return 7
    return 8


# FIX (Bugs #9, #10): Refactored from app.py with Claude Code agent mode and added
# the low/high range so negative or out-of-range guesses are rejected.
def parse_guess(raw: str, low: int = 1, high: int = 100):
    """
    Parse user input into an int guess within [low, high].

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: whitespace-only input ("   ") now counts as empty too
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    raw = raw.strip()

    try:
        value = int(raw)
    except ValueError:
        # FIX (Bug #10): "42.7" used to be silently cut to 42; the AI suggested
        # trying float() to tell a decimal apart from text and warn the player.
        try:
            float(raw)
        except ValueError:
            return False, None, "That is not a number."
        return False, None, "Please enter a whole number (no decimals)."

    # FIX (Bug #9): no range check before, so -5 or 500 were accepted
    if value < low or value > high:
        return False, None, f"Your guess must be between {low} and {high}."

    return True, value, None


# FIX (Bug #5): Moved from app.py into logic_utils.py using Claude Code agent mode.
def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX (Bug #6): removed the try/except TypeError fallback that compared the
    # numbers as text ("9" > "50"); app.py now always passes the secret as an int.
    if guess > secret:
        # FIX (Bug #5): the messages were swapped ("Too High" said "Go HIGHER!")
        return "Too High", "📉 Too high! Go LOWER!"
    return "Too Low", "📈 Too low! Go HIGHER!"


# FIX (Bug #11): Refactored from app.py with Claude Code agent mode.
def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number (1 = first guess)."""
    if outcome == "Win":
        # FIX: was (attempt_number + 1), so a first-guess win scored 70 instead of 100
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    # FIX: "Too High" on even attempts used to ADD 5 points; now every miss costs 5
    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
