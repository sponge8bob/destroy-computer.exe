from destroy_computer_exe.games.wordle import _score, _daily_word, _letter_statuses
from datetime import date


def test_all_correct():
    assert _score("CRANE", "CRANE") == ["correct"] * 5


def test_all_absent():
    assert _score("BITSY", "CROWN") == ["absent"] * 5


def test_present_letters():
    # ACORN vs CRANE: A,C,R,N all in CRANE but at wrong positions; O absent
    result = _score("ACORN", "CRANE")
    assert result == ["present", "present", "absent", "present", "present"]


def test_exact_beats_present():
    # CRANE vs CRANE — all correct, not present
    result = _score("CRANE", "CRANE")
    assert all(s == "correct" for s in result)


def test_duplicate_not_double_counted():
    # SPEED vs CREEP: S absent, P present (at pos4 in answer), E correct x2, D absent
    result = _score("SPEED", "CREEP")
    assert result == ["absent", "present", "correct", "correct", "absent"]


def test_duplicate_answer_limited():
    # BOOST vs ROBOT: B present, O correct (pos1), O present (pos3 in answer), S absent, T absent
    # ROBOT = R O B O T  (two O's)
    # BOOST = B O O S T
    # pos0: B vs R -> B in ROBOT at pos2 -> present
    # pos1: O vs O -> correct, consume ROBOT[1]
    # pos2: O vs B -> O in remaining ROBOT (pos3) -> present, consume
    # pos3: S vs O -> S not in remaining -> absent
    # pos4: T vs T -> correct
    result = _score("BOOST", "ROBOT")
    assert result == ["present", "correct", "present", "absent", "correct"]


def test_daily_word_deterministic():
    # Same date always gives same word
    from destroy_computer_exe.games.wordle import _load_words
    answers = _load_words("wordle_answers.txt")
    w1 = _daily_word(answers)
    w2 = _daily_word(answers)
    assert w1 == w2
    assert len(w1) == 5


def test_letter_statuses_priority():
    # Best status is kept even if a later guess gives a worse result
    guesses = [
        ("CRANE", ["correct", "present", "absent", "absent", "absent"]),  # R=present
        ("CRONE", ["correct", "absent",  "absent", "absent", "absent"]),  # R=absent (should not downgrade)
    ]
    statuses = _letter_statuses(guesses)
    assert statuses["C"] == "correct"
    assert statuses["R"] == "present"   # stays present, not downgraded
    assert statuses.get("A") in (None, "absent")
