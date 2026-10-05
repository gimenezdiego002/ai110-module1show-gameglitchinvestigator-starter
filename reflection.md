# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I first ran the game, it was very simple and had multiple bugs that made it hard, and sometimes impossible, to play correctly. The hints were wrong, attempts were already missing before I even guessed, and starting a new game after winning did not reset everything. I also noticed that negative numbers and decimals could be entered even though they should not be valid guesses. The game technically ran, but a lot of the logic behind it was broken.

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 60 when the secret is 50 | Tell me the guess is too high and to go lower | The hint told me to go higher instead | No console error; the game logic was incorrect |
| Click New Game after winning | Reset the game and let me play again | The game still acted like I had already won and would not restart | No console error; session state was not fully reset |
| Enter `42.7` | Reject the guess because it is a decimal | The game changed the decimal into a whole number and accepted it | No console error; input validation was incorrect |
| Start a Normal game | Start with 8 attempts available | It showed only 7 attempts before I even guessed | No console error; the attempt counter started at the wrong value |

---

## 2. How did you use AI as a teammate?

I mainly used Claude to help make the code changes and fix the bugs, and I used ChatGPT when I got stuck or needed something explained differently. Most of Claude's suggestions were correct because I reviewed the code myself first and understood what I wanted changed before writing the prompt.

**A suggestion that was correct:** Claude moved the `check_guess` logic into `logic_utils.py` and fixed the high and low hints, which had been swapped. I verified it by running the game and testing guesses above and below the secret number. The hints now pointed in the right direction.

**A suggestion I did not accept as written:** Claude suggested making the debug panel visible with a checkbox that the player could toggle. I rejected that because a player could just click it and see the secret number. Instead, I insisted the debug info only show up if the developer sets an environment variable (`GAME_DEBUG=1`) before starting the app. This way, players cannot accidentally—or intentionally—cheat by checking the debug box. I verified it by running the app normally (no debug panel) and then with `GAME_DEBUG=1` (panel appears).
---

## 3. Debugging and testing your fixes

I decided a bug was actually fixed by first reviewing the code changes and then running the Streamlit app again to test the same thing that was broken before. I tried to reproduce the original bug and made sure it now behaved correctly before making more changes. This helped me make sure that fixing one problem did not create another one.

I also ran `python -m pytest` to test the game logic. Pytest runs small automatic tests that check whether functions return what they are supposed to. At the beginning the tests failed because some of the functions in `logic_utils.py` were still placeholders. After the changes there were 14 tests, and all 14 passed. This showed me that checking guesses, validating input, difficulty ranges and scoring were all behaving correctly.

AI also helped me understand what the tests were checking. Instead of only seeing that a test passed or failed, I could ask why it failed and what input the test was giving the function. That made pytest easier to understand, because it felt like automatically trying different situations in the game instead of testing everything manually.

---

## 4. What did you learn about Streamlit and state?

The easiest way I would explain Streamlit reruns is that almost every time you click something or change an input, Streamlit runs the Python file again from the top. Because of that, normal variables get recreated or lost. `st.session_state` is like a memory box that keeps important information between those reruns, such as the secret number, attempts, score, history, and whether the player already won. This project showed me that if session state is not reset or updated correctly, the app can look fine but still behave wrong.

---

## 5. Looking ahead: your developer habits

One habit I want to keep is fixing and testing bugs one at a time instead of asking AI to change the whole project at once. I also want to keep reviewing the before and after code, because it helped me understand what the AI actually changed instead of just trusting that it worked. Running the program and pytest after changes is also something I will do again.

Next time I work with AI on a coding task, I would be even more specific with my prompts from the beginning and tell it exactly which bug I want fixed and which files it should or should not change.

This project changed the way I think about AI-generated code. AI can make coding a lot faster, but I still need to understand, review and test what it generates. Just because the code runs does not mean the logic is correct.
