# Cooling assignment: lecture slides

Starter decks for the four parts of the cooling assignment (`assignments/cooling/`), on the DTU template from lecture 13.1.

| Deck | Part |
|---|---|
| `lecture-1-window-size-automoo.pptx` | 1: Window size with IDA ICE AutoMOO |
| `lecture-2-venting-hatch-draught.pptx` | 2: Venting hatches without draught (incl. Heiselberg et al. 1999 window study) |
| `lecture-3-ceiling-fans.pptx` | 3: Ceiling fans for peak periods |
| `lecture-4-shutters-heatwave.pptx` | 4: Shutters and fans in a heat wave |

Status: drafts. Lecture 2 has been reviewed in part; lectures 1, 3 and 4 have not been checked yet and still follow an earlier outline (`deck-outlines.md` is the current plan; lecture 3 does not yet have the fan COP slide in its approved form). Slides marked "TO DEVELOP" are placeholders for IDA ICE screenshots or worked examples.

## Rebuilding

- `code/make_figures.py`: charts from the Annex 80 EPW files and the course models (needs matplotlib, scipy, pythermalcomfort).
- `code/window_types_figure.py`: schematic of the three Heiselberg et al. (1999) window types.
- `code/build_decks.py` with `code/deck_lib.py`: builds the decks with python-pptx. Paths point to the project folder (EPWs, the lecture 13.1 template, draft figures); adjust them before running elsewhere. `--deck2` rebuilds lecture 2 only.
