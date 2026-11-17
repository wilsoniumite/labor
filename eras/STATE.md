# STATE — eras (resume point)

**Thread:** rough shapes and sizes of the task schedule through history: the machines' region, the ceiling, the
contestable band, H. Started 2026-11-17 at her ask ("just to take a look, might be a paper down the line"; "I leave
all the other decisions up to you"). Nothing here touches `../pinning/`.

**Read first:** `REPORT.md`: findings ranked from firmest to roughest, sources, assumptions, what was not reached.

**Run:** from `eras/`, with numpy, pandas, matplotlib, openpyxl, requests (`../venv` on her machine; the session used a
scratch venv): `code/pull.py`, `code/machines_region.py`, `code/skeleton.py`, `code/modern_schedule.py`,
`code/eras.py`. `pull.py` caches the two downloads in `cache/` (gitignored) and stops if either is unreachable.

## State as of 2026-11-17

Done: Warde's energy series parsed (1560–1870) and the Bank of England millennium dataset's series pulled; the machines'
region by power accounting (1700–1870) and by the model's reading of output per hour (1870–2016); the ceiling and
contestable band through time (US machinery 1967–2023, UK proxy 1855–2016); the 1999–2025 US schedule from the
companion's revealed adoption, with the 2025 split by LLM exposure; the long-run traced schedule; four figures.

Not reached: the Hand and Machine Labor microdata (openICPSR, HTTP 403 here; only the JEP article's published mean is
used). No substitute was taken.

## Open (her calls)

1. Worth a paper? Findings 1–4 (the ceiling's height, the band's width, 1999–2025, the 2025 split) are data-backed.
   Finding 5's reading after 1870 and finding 6 lean on the model's own accounting.
2. If yes: Leontief's 1919/1929 tables, the HML microdata (her openICPSR login), and a hedonic machinery price series
   are the three sources that would move it from rough to measured.
