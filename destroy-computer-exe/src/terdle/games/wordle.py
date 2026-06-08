from __future__ import annotations

from datetime import date
from importlib.resources import files

from rich.align import Align
from rich.panel import Panel
from rich.text import Text

from terdle.ui.theme import BOARD_STYLES, KEY_STYLES, console

WORD_LENGTH = 5
MAX_GUESSES = 6
KEYBOARD_ROWS = ("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM")
EMOJI: dict[str, str] = {"correct": "🟩", "present": "🟨", "absent": "⬛"}
_WIN_LABELS = ("Genius!", "Magnificent!", "Impressive!", "Splendid!", "Great!", "Phew!")
_SCORE_PRIORITY = {"correct": 3, "present": 2, "absent": 1}


def _load_words(filename: str) -> list[str]:
    text = files("terdle").joinpath("data").joinpath(filename).read_text(encoding="utf-8")
    return sorted({w.strip().upper() for w in text.splitlines() if len(w.strip()) == WORD_LENGTH})


def _daily_word(answers: list[str]) -> str:
    delta = (date.today() - date(2021, 6, 19)).days
    return answers[delta % len(answers)]


def _score(guess: str, answer: str) -> list[str]:
    result = ["absent"] * WORD_LENGTH
    pool = list(answer)
    # First pass: exact matches
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            result[i] = "correct"
            pool[i] = None
    # Second pass: present-but-wrong-position (consume pool entries to avoid double-counting)
    for i, g in enumerate(guess):
        if result[i] != "correct" and g in pool:
            result[i] = "present"
            pool[pool.index(g)] = None
    return result


def _letter_statuses(guesses: list[tuple[str, list[str]]]) -> dict[str, str]:
    statuses: dict[str, str] = {}
    for word, scores in guesses:
        for letter, score in zip(word, scores):
            if _SCORE_PRIORITY[score] > _SCORE_PRIORITY.get(statuses.get(letter, "absent"), 0):
                statuses[letter] = score
    return statuses


def _render(guesses: list[tuple[str, list[str]]], message: str = "") -> None:
    console.clear()
    console.rule("[bold white]T E R D L E[/bold white]", style="dim white")
    console.print()

    for i in range(MAX_GUESSES):
        row = Text()
        if i < len(guesses):
            word, scores = guesses[i]
            for j, (letter, score) in enumerate(zip(word, scores)):
                if j:
                    row.append(" ")
                row.append(f" {letter} ", style=BOARD_STYLES[score])
        else:
            for j in range(WORD_LENGTH):
                if j:
                    row.append(" ")
                row.append("   ", style=BOARD_STYLES["empty"])
        console.print(Align.center(row))
        console.print()  # slight row gap

    statuses = _letter_statuses(guesses)
    for i, row_str in enumerate(KEYBOARD_ROWS):
        row = Text()
        for j, letter in enumerate(row_str):
            if j:
                row.append(" ")
            row.append(f" {letter} ", style=KEY_STYLES[statuses.get(letter, "unseen")])
        console.print(Align.center(row))
        if i < len(KEYBOARD_ROWS) - 1:
            console.print()  # slight row gap

    console.print()

    if message:
        console.print(Align.center(f"[bold]{message}[/bold]"))
        console.print()


def _share_text(guesses: list[tuple[str, list[str]]], answer: str) -> str:
    today = date.today().isoformat()
    won = bool(guesses) and guesses[-1][0] == answer
    score_str = f"{len(guesses)}/6" if won else "X/6"
    rows = [f"TERdle Wordle  {today}  {score_str}", ""]
    for _, scores in guesses:
        rows.append("".join(EMOJI[s] for s in scores))
    return "\n".join(rows)


def play() -> None:
    answers = _load_words("wordle_answers.txt")
    valid = set(_load_words("wordle_valid.txt")) | set(answers)
    answer = _daily_word(answers)

    guesses: list[tuple[str, list[str]]] = []
    message = ""

    while len(guesses) < MAX_GUESSES:
        _render(guesses, message)
        message = ""

        console.print(Align.center("[dim]guess a 5-letter word →[/dim]"))
        raw = input("   > ").strip().upper()

        if not raw:
            continue
        if len(raw) != WORD_LENGTH:
            message = f"Word must be exactly {WORD_LENGTH} letters"
            continue
        if raw not in valid:
            message = "Not in word list"
            continue

        scores = _score(raw, answer)
        guesses.append((raw, scores))

        if raw == answer:
            break

    won = bool(guesses) and guesses[-1][0] == answer
    _render(guesses)

    if won:
        label = _WIN_LABELS[len(guesses) - 1]
        console.print(Align.center(f"[bold green]{label}[/bold green]"))
    else:
        console.print(Align.center(f"[bold]The word was [green]{answer}[/green][/bold]"))

    console.print()
    share = _share_text(guesses, answer)
    console.print(Align.center(Panel(share, title="[dim]share[/dim]", expand=False, border_style="dim")))
    console.print()
