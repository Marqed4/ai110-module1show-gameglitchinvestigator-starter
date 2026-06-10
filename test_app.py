import pytest
from app import get_range_for_difficulty, parse_guess, check_guess, update_score

EASY_LOW, EASY_HIGH = 1, 20
EASY_ATTEMPT_LIMIT = 8


# --- get_range_for_difficulty ---

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_easy_secret_within_range():
    import random
    low, high = get_range_for_difficulty("Easy")
    for _ in range(100):
        secret = random.randint(low, high)
        assert EASY_LOW <= secret <= EASY_HIGH


# --- parse_guess ---

def test_parse_guess_valid_easy_boundary_low():
    ok, value, err = parse_guess("1")
    assert ok is True
    assert value == 1
    assert err is None


def test_parse_guess_valid_easy_boundary_high():
    ok, value, err = parse_guess("20")
    assert ok is True
    assert value == 20
    assert err is None


def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


def test_parse_guess_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


# --- check_guess ---

def test_check_guess_correct():
    outcome, message = check_guess(10, 10)
    assert outcome == "Win"


def test_check_guess_too_high():
    outcome, _ = check_guess(15, 8)
    assert outcome == "Too High"


def test_check_guess_too_low():
    outcome, _ = check_guess(3, 18)
    assert outcome == "Too Low"


# --- update_score (Easy: 8 attempts, range 1–20) ---

def test_update_score_win_first_attempt():
    # attempts starts at 1, incremented to 2 before update_score is called
    score = update_score(0, "Win", 2)
    assert score == 70  # 100 - 10*(2+1) = 70


def test_update_score_wrong_guesses_deplete_score():
    score = 0
    for attempt in range(2, EASY_ATTEMPT_LIMIT + 2):
        score = update_score(score, "Too Low", attempt)
    assert score == -5 * EASY_ATTEMPT_LIMIT
