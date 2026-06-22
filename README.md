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

- [x] Describe the game's purpose. A number guessing game where the player picks a difficulty, gets a secret number within that range, and guesses until they win or run out of attempts. Hints tell you whether to guess higher or lower.
- [x] Detail which bugs you found. Hints were backwards due to string vs int comparison on even attempts. The New Game button ignored difficulty and always used range 1-100. Switching difficulty mid-game kept the old secret, making the game unwinnable. The Hard difficulty range was narrower than Normal. Session state (score, status, history) was not reset on new game.
- [x] Explain what fixes you applied. Fixed comparison by always casting secret to int and removing the string conversion. Fixed New Game and difficulty switching to regenerate the secret within the correct range. Fixed Hard range to be the widest (1-100). Reset all session state on new game. Refactored all logic into logic_utils.py.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Run `python -m streamlit run app.py` and open the app in your browser.
2. Select a difficulty from the sidebar. Easy gives a range of 1-20 with 8 attempts, Normal is 1-50 with 6, Hard is 1-100 with 5.
3. Open the "Developer Debug Info" panel to see the secret number and confirm it falls within the selected difficulty range.
4. Type a guess and click Submit. The hint correctly tells you to go higher or lower based on your guess.
5. Keep guessing until you win or run out of attempts. Click New Game to reset everything and start fresh with a new secret in the current difficulty range.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest tests/test_game_logic.py test_app.py -v
============================= test session starts =============================
platform win32 -- Python 3.13.12, pytest-9.0.3, pluggy-1.6.0
collected 14 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  7%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 14%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 21%]
test_app.py::test_easy_range PASSED                                      [ 28%]
test_app.py::test_easy_secret_within_range PASSED                        [ 35%]
test_app.py::test_parse_guess_valid_easy_boundary_low PASSED             [ 42%]
test_app.py::test_parse_guess_valid_easy_boundary_high PASSED            [ 50%]
test_app.py::test_parse_guess_empty_string PASSED                        [ 57%]
test_app.py::test_parse_guess_non_numeric PASSED                         [ 64%]
test_app.py::test_check_guess_correct PASSED                             [ 71%]
test_app.py::test_check_guess_too_high PASSED                            [ 78%]
test_app.py::test_check_guess_too_low PASSED                             [ 85%]
test_app.py::test_update_score_win_first_attempt PASSED                  [ 92%]
test_app.py::test_update_score_wrong_guesses_deplete_score PASSED        [100%]

============================== 14 passed in 0.72s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
