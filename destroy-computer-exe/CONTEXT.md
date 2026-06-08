# TERdle — Terminal DLE Games

A command-line application for playing daily-style word and puzzle games ("DLE" games) in the terminal.

---

## Vision

A single CLI entry point that lets users launch and play multiple DLE-style games. Each game runs interactively in the terminal with keyboard input, colored output, and a clean UI. Games share infrastructure (word lists, rendering, session state) but have independent logic.

---

## Planned Games

| Game | Description | Status |
|------|-------------|--------|
| Wordle | Guess a 5-letter word in 6 tries with color-coded feedback | Planned |
| Connections | Group 16 words into 4 categories of 4 | Planned |

---

## Tech Stack

> To be decided. Options:
> - **Python** — rich library for color/layout, fast to prototype
> - **Node.js / TypeScript** — familiar if JS-oriented, blessed/ink for TUI
> - **Go** — single binary, tcell/bubbletea for TUI

---

## CLI Interface

```
terdle                    # Show game menu
terdle wordle             # Launch Wordle directly
terdle connections        # Launch Connections directly
terdle --help             # Show help
```

---

## Shared Features

- Color output (green/yellow/grey for Wordle; colour-coded categories for Connections)
- Daily seed (same puzzle for everyone on a given date, deterministic from date)
- Local session persistence (track streaks, history)
- Share result (copy emoji grid to clipboard, like real Wordle)
- Keyboard-driven input (no mouse required)

---

## Wordle Spec

- 5-letter word, 6 attempts
- After each guess:
  - **Green**: correct letter, correct position
  - **Yellow**: correct letter, wrong position
  - **Grey**: letter not in word
- Hard mode option: must use revealed hints in subsequent guesses
- Word list: curated ~2500 answer words + larger valid-guess dictionary

---

## Connections Spec

- 16 words arranged in a 4×4 grid
- Player groups them into 4 sets of 4, each sharing a hidden category
- 4 difficulty tiers (colour-coded: yellow / green / blue / purple)
- 4 mistakes allowed before game over
- After each guess: told if correct (category revealed) or wrong (how many away: "One away!")

---

## Project Structure (proposed)

```
TERdle/
├── CONTEXT.md          # This file — specs and design decisions
├── src/
│   ├── main.*          # Entry point, game menu
│   ├── games/
│   │   ├── wordle.*
│   │   └── connections.*
│   ├── ui/             # Shared rendering/color utilities
│   └── data/           # Word lists, puzzle seeds
├── tests/
└── README.md
```

---

## Design Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-06-08 | Project created | — |

---

## Open Questions

- [ ] Which language/runtime?
- [ ] Daily seed source (date-based hash? remote API?)
- [ ] Where to persist session data (local file, sqlite)?
- [ ] Puzzle data: curated static files vs. scraped/generated?
