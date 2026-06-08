from rich.console import Console
from rich.style import Style

console = Console()

# Board cell styles (Wordle dark-mode palette)
CORRECT = Style(color="white", bgcolor="#538d4e", bold=True)
PRESENT = Style(color="white", bgcolor="#b59f3b", bold=True)
ABSENT  = Style(color="white", bgcolor="#3a3a3c", bold=True)
EMPTY   = Style(color="#565758", bgcolor="#121213")

# Keyboard key styles
KEY_UNSEEN  = Style(color="white",   bgcolor="#818384", bold=True)
KEY_ABSENT  = Style(color="#3a3a3c", bgcolor="#1a1a1b")           # sunken/dark — used & not in word

BOARD_STYLES: dict[str, Style] = {
    "correct": CORRECT,
    "present": PRESENT,
    "absent":  ABSENT,
    "empty":   EMPTY,
}

KEY_STYLES: dict[str, Style] = {
    "correct": CORRECT,
    "present": PRESENT,
    "absent":  KEY_ABSENT,
    "unseen":  KEY_UNSEEN,
}
