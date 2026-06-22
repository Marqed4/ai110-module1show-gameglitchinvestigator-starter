# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it appeared to work on the surface but produced incorrect behavior almost immediately. The hints were backwards — guessing too high would tell you to go higher, and guessing too low would tell you to go lower. The difficulty setting had no real effect because the "New Game" button always generated a secret between 1 and 100 regardless of the selected range, and the Hard difficulty range was actually narrower than Normal, making it easier instead of harder. Additionally, switching difficulty mid-game would leave the existing secret in place even if it fell completely outside the new range, making the game unwinnable.

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  1. incorrect target secret
  2. incorrect comparison fixed by a cast to int
  3. fixed leveldifficulty

**Bug Reproduction Log**

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess 39, secret is 9 (even attempt) | "Go LOWER" hint | "Go HIGHER" hint | No error — wrong string comparison silently returned wrong result |
| Switch difficulty from Normal to Easy mid-game, secret was 85 | New secret generated within 1–20 | Old secret 85 stays, player can never win | No error — secret just out of range |
| Click "New Game" on Hard difficulty | Secret generated within Hard range (1–100) | Secret always generated between 1–100 ignoring difficulty | No error — `random.randint(1, 100)` hardcoded |

---

## 2. How did you use AI as a teammate?

I used Claude Code (via the Claude Code CLI) as my primary AI assistant throughout this project. One example of a correct and useful suggestion: Claude identified that on even-numbered attempts the secret was being cast to a string, causing the comparison `"39" > "9"` to use lexicographic ordering instead of numeric ordering — which explained why hints were backwards on those attempts. I verified this by tracing the logic manually: `"3" < "9"` alphabetically, so `"39"` was treated as less than `"9"`, returning "Too Low / Go Higher" when the guess was actually higher than the secret. An example of a suggestion I pushed back on: Claude initially suggested resetting `attempts` to `0` to fix the off-by-one in the attempt counter display, but I preferred keeping it 1-based, so we adjusted the display formula and game-over check instead to stay consistent with that convention.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed when I could trace through the logic manually and confirm the correct output, and then verified with a pytest that exercised the exact scenario. For the hint direction bug, the test `test_check_guess_too_high` confirmed that passing a guess larger than the secret returns `"Too High"` — before the fix, the string-comparison fallback path would have returned the wrong outcome. For the scoring, `test_update_score_win_first_attempt` locked in that winning on the first real attempt (attempt number 2 in 1-based counting) returns a score of 70, catching any future regression in that formula. Claude helped me understand what to assert in each test by explaining what the function should return given specific inputs, which made it easier to write precise assertions rather than just checking that the function ran without crashing.

---

## 4. What did you learn about Streamlit and state?

Streamlit reruns the entire Python script from top to bottom every time a user interacts with the app — clicking a button, typing in a field, or changing a selectbox all trigger a full rerun. Because of this, regular Python variables reset on every rerun, so Streamlit provides `st.session_state` as a dictionary-like object that persists values across reruns. One subtle bug this caused: switching the difficulty selectbox triggered a rerun, but the secret stored in session state was from the old difficulty range and never got regenerated — the fix was to detect when the difficulty value changed and reset the game state at the top of the script before anything else ran. Without understanding reruns, bugs like that are very hard to reason about because the code looks correct in isolation.

---

## 5. Looking ahead: your developer habits

One habit I want to carry forward is writing tests immediately after fixing a bug — not as an afterthought — so the fix is locked in and can't quietly regress later. The pytest suite we wrote for Easy mode gave me a fast way to confirm that the core logic (range, parsing, hint direction, scoring) was all working correctly at once. Next time I work with AI on a coding task, I would ask it to explain *why* a bug exists before applying the fix, rather than just accepting the first suggested change — understanding the root cause helped me make better decisions, like keeping attempts 1-based instead of blindly resetting to 0. This project changed how I think about AI-generated code: it can introduce plausible-looking bugs that pass a quick read but fail in specific runtime conditions, so treating AI output as a first draft that needs testing rather than finished code is the right mindset.
