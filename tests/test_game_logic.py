from logic_utils import (
    check_guess,
    get_attempt_limit,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

# FIX (Bug #12): check_guess returns (outcome, message), but the original tests
# compared the whole pair to "Win". The AI and I unpacked the outcome instead.
def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

# FIX: tests below were added with the AI to cover each bug that was fixed
def test_small_number_is_too_low_not_compared_as_text():
    # As text, "9" > "50"; as numbers, 9 < 50
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"

def test_difficulty_ranges_get_harder():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)

def test_easier_difficulty_gives_more_attempts():
    assert get_attempt_limit("Easy") > get_attempt_limit("Normal") > get_attempt_limit("Hard")

def test_parse_valid_guess():
    assert parse_guess("42", 1, 100) == (True, 42, None)
    assert parse_guess("  7 ", 1, 100) == (True, 7, None)

def test_parse_empty_guess():
    ok, _, err = parse_guess("", 1, 100)
    assert not ok
    assert err == "Enter a guess."

def test_parse_rejects_text():
    ok, _, err = parse_guess("abc", 1, 100)
    assert not ok
    assert err == "That is not a number."

def test_parse_rejects_decimal():
    ok, _, err = parse_guess("42.7", 1, 100)
    assert not ok
    assert "whole number" in err

def test_parse_rejects_negative_and_out_of_range():
    for raw in ("-5", "0", "101"):
        ok, _, err = parse_guess(raw, 1, 100)
        assert not ok
        assert err == "Your guess must be between 1 and 100."

def test_first_guess_win_scores_100():
    assert update_score(0, "Win", 1) == 100

def test_win_score_never_below_10():
    assert update_score(0, "Win", 50) == 10

def test_wrong_guesses_always_lose_points():
    for attempt in (1, 2, 3, 4):
        assert update_score(0, "Too High", attempt) == -5
        assert update_score(0, "Too Low", attempt) == -5
