# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

### Game Purpose

The player picks a difficulty (Easy 1–20, Normal 1–50 or Hard 1–100), and the game chooses a secret number in that range. The player has a limited number of attempts to guess it. After each wrong guess, a hint should say whether the guess was **too high** or **too low**. A correct guess wins the game and gives a score based on how few attempts it took. **New Game** should reset everything so the player can play again.

### Bugs Found

*Line numbers refer to the original starter code.*

| # | Bug | Where | Cause |
|---|-----|-------|-------|
| 1 | **Can't play again after winning.** Clicking "New Game" still shows "You already won." | `app.py` lines 134–145 | New Game resets attempts and the secret but never sets `status` back to `"playing"`. It also doesn't reset score or history, and the new secret is always 1–100 whatever the difficulty. |
| 2 | **Attempts start at 7 instead of 8 (Normal).** | `app.py` line 96 | `attempts` starts at `1` instead of `0`. |
| 3 | **"Attempts left" is one click behind.** | `app.py` lines 109–112 | The info box is drawn *before* the guess is processed. |
| 4 | **Invalid input uses up an attempt.** | `app.py` line 148 | The attempt counter goes up before the input is checked. |
| 5 | **Hints are backwards.** A guess that is too high says "Go HIGHER!", and a guess that is too low says "Go LOWER!". | `check_guess`, lines 37–40 | The two messages are swapped. |
| 6 | **Hints are wrong on every other guess.** | `app.py` lines 158–161 | On even attempts the secret is turned into text, so numbers are compared alphabetically (e.g. `"9" > "50"`). |
| 7 | **Developer Debug Info shows the secret to the player.** | `app.py` lines 114–119 | The debug panel is always visible and prints the secret. |
| 8 | **Difficulty is hard to find and doesn't work.** | `app.py` lines 4–11, 74–90, 110 | The selector is only in the sidebar, which can be collapsed. Hard (1–50) is easier than Normal (1–100), and Easy gets fewer attempts (6) than Normal (8). Changing difficulty doesn't pick a new secret, so on Easy (1–20) the secret can still be 87. The prompt always says "between 1 and 100". |
| 9 | **Negative and out-of-range numbers are accepted.** | `parse_guess`, lines 14–29 | There is no range check, so `-5` or `500` is accepted and costs an attempt. |
| 10 | **Decimals are quietly cut off.** | `parse_guess`, lines 22–23 | `"42.7"` becomes `42` with no warning. |
| 11 | **Scoring is broken.** | `update_score`, lines 50–65 | The win formula uses `attempt_number + 1`, so it under-scores. A "Too High" guess on an even attempt *adds* 5 points. |
| 12 | **Tests can't pass.** | `logic_utils.py`, `tests/test_game_logic.py` | The functions in `logic_utils.py` are placeholders that raise `NotImplementedError`. The tests also expect `check_guess` to return `"Win"`, but it returns a pair like `("Win", "🎉 Correct!")`. |

### Fixes Applied

Every fix is marked with a `# FIX (Bug #N):` comment in the code. The logic now lives in `logic_utils.py`, and `app.py` only handles the UI.

| Bug | Fix | File |
|-----|-----|------|
| #1 New Game blocked after winning | New `start_new_game()` resets **everything** (secret, attempts, score, status, history). It is used by New Game and when difficulty changes. `st.stop()` was replaced by disabling Submit once the game ends. | `app.py` |
| #2 Attempts started at 7 | `attempts` starts at `0`, so Normal shows 8. | `app.py` |
| #3 "Attempts left" lagged a click behind | A spot is reserved with `status_box = st.container()` and filled in *after* the guess is processed. | `app.py` |
| #4 Invalid input cost an attempt | `attempts += 1` only runs after `parse_guess` accepts the input. | `app.py` |
| #5 Hints were backwards | Messages swapped to `"📉 Too high! Go LOWER!"` and `"📈 Too low! Go HIGHER!"`. | `logic_utils.py` |
| #6 Wrong hints on every other guess | Removed the code that turned the secret into text on even attempts, plus the `try/except TypeError` fallback that compared text (`"9" > "50"`). | `app.py`, `logic_utils.py` |
| #7 Debug panel showed the secret | Only shown if the app is started with `GAME_DEBUG=1`, e.g. `$env:GAME_DEBUG="1"; python -m streamlit run app.py`. | `app.py` |
| #8 Difficulty hidden and backwards | Moved to a radio button on the main page. Ranges are now Easy 1–20, Normal 1–50, Hard 1–100. Attempts are Easy 10, Normal 8, Hard 7. Changing difficulty starts a new game in the new range, and all text uses the real range. | `app.py`, `logic_utils.py` |
| #9 Negative / out-of-range guesses accepted | `parse_guess(raw, low, high)` rejects them: *"Your guess must be between 1 and 50."* | `logic_utils.py` |
| #10 Decimals quietly cut off | `"42.7"` is rejected: *"Please enter a whole number (no decimals)."* | `logic_utils.py` |
| #11 Broken scoring | A first-guess win scores 100 (−10 per extra guess, minimum 10). Every wrong guess costs 5 points. | `logic_utils.py` |
| #12 Tests couldn't pass | Moved all four functions into `logic_utils.py` (plus a new `get_attempt_limit`). Tests unpack `(outcome, message)`, and 11 new tests were added. | `logic_utils.py`, `tests/` |

**Extra:** With "Show hint" unchecked, a wrong guess now shows *"❌ Not quite. Try again!"* instead of nothing. The guess box also clears on each new game.

## 📸 Demo Walkthrough

### Before: the broken game

Steps I took while playing the **broken** game, showing how each bug appeared:

1. **Start the game.** Ran `python -m streamlit run app.py` and opened it on localhost. "Attempts left" already said **7** before my first guess, even though Normal allows 8.
2. **Enter a negative number.** Typed `-5` and clicked Submit. The game accepted it, used up an attempt and added it to history, even though it's outside 1–100. There was no "out of range" message.
3. **Enter a decimal.** Typed `42.7`. The game quietly treated it as `42` and used up an attempt, with no warning that decimals aren't allowed.
4. **Use the hint.** With "Show hint" checked, the hints were no help. A guess above the secret said "Go HIGHER!" and one below said "Go LOWER!", which is the wrong direction. On every second guess the hint was wrong in a different way, because the game compares the numbers as text.
5. **Look for difficulty.** I couldn't see an Easy, Normal or Hard option on the page, because it's only in the collapsible sidebar. When I did change it, the secret didn't change, and the page still said "Guess a number between 1 and 100."
6. **Win, then try again.** I guessed the number (the Developer Debug Info panel shows it to anyone). Then I clicked "New Game", but it kept saying **"You already won. Start a new game to play again."**, so the game couldn't be replayed.

### After: the fixed game

1. **Start the game.** Run `python -m streamlit run app.py`. The Easy / Normal / Hard choice is at the top of the page, with the range and attempts allowed shown below it. On Normal, the box says *"Guess a number between 1 and 50. Attempts left: 8"*. There is no debug panel giving away the answer.
2. **Enter a negative number.** Typing `-5` shows *"Your guess must be between 1 and 50."* and does not use an attempt.
3. **Enter a decimal.** Typing `42.7` shows *"Please enter a whole number (no decimals)."* and does not use an attempt.
4. **Use the hint.** A wrong guess shows the correct direction, e.g. *"📈 Too low! Go HIGHER!"*, and "Attempts left" goes down by one straight away.
5. **Change difficulty.** Switching to Easy starts a new game with a secret between 1 and 20 and 10 attempts.
6. **Win, then play again.** Guessing the number shows balloons and *"🎉 You won in N guess(es)! ... Final score: X"*. Clicking **New Game** resets everything and you can play again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

Before any fixes:

```
pytest tests/
FAILED tests/test_game_logic.py::test_winning_guess - NotImplementedError: Re...
FAILED tests/test_game_logic.py::test_guess_too_high - NotImplementedError: R...
FAILED tests/test_game_logic.py::test_guess_too_low - NotImplementedError: Re...
========================= 3 failed in 0.46s =========================
```

After the fixes:

```
pytest tests/ -v
tests/test_game_logic.py::test_winning_guess PASSED
tests/test_game_logic.py::test_guess_too_high PASSED
tests/test_game_logic.py::test_guess_too_low PASSED
tests/test_game_logic.py::test_small_number_is_too_low_not_compared_as_text PASSED
tests/test_game_logic.py::test_difficulty_ranges_get_harder PASSED
tests/test_game_logic.py::test_easier_difficulty_gives_more_attempts PASSED
tests/test_game_logic.py::test_parse_valid_guess PASSED
tests/test_game_logic.py::test_parse_empty_guess PASSED
tests/test_game_logic.py::test_parse_rejects_text PASSED
tests/test_game_logic.py::test_parse_rejects_decimal PASSED
tests/test_game_logic.py::test_parse_rejects_negative_and_out_of_range PASSED
tests/test_game_logic.py::test_first_guess_win_scores_100 PASSED
tests/test_game_logic.py::test_win_score_never_below_10 PASSED
tests/test_game_logic.py::test_wrong_guesses_always_lose_points PASSED
========================= 14 passed in 0.04s =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
