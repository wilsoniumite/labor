# Option documents

Side-by-side documents for choosing, with Johan, between versions of the paper's main text. Each document is
printed landscape (A4). Each row is one topic; its options sit side by side, so the authors can mix and match.

- **Part 1 — layouts of the whole paper.** A map (content blocks down, layouts across, each cell the section that
  holds the block), then the layouts' outlines four to a row. S1 is the rewrite, S2 the original without its
  Section 2; S3 onward are new. Every layout keeps all of the main text's content.
- **Part 2 — the model at three levels.** Simple, Medium and Complex (the rewrite) versions of Sections 2–6, row
  by row. In every version the appendix carries the full Complex treatment, so a lower level moves material and
  loses none. Each column read top to bottom is a complete main text at its level.
- **Part 3 — the text, part by part.** Rewrite (R), original without Section 2 (O), and new options (N1, N2).
  3.1 is the introduction; the numerical economy, measurement, history and stabilizers, and AI and the conclusion
  follow.

## Rules the documents follow

- Every option is a real difference from the others in its row: content, order, framing, device or level of
  formality, not wording. Text that two options share prints once; a level that keeps another's text with only
  numbering or one sentence changed joins its cell, with a note saying what changes.
- A row with a single option has a column for comments and, where it applies, the reason it has no alternative
  ("can't change", "no better idea yet"; "loved" is Stella's call).
- No cuts for now: options may add content, not remove it.
- New text follows Stella's and Johan's style rules: plain prose, no figurative language, no "load-bearing", no em
  dashes, no "not X but Y", no stock words, no "turns". `lint_options.py` flags these and near-rewordings (word
  similarity above 0.75 to another option of the row); a flagged cell stays only when its difference is real.
- R and O are extracted from `paper/main_rewrite.tex` and `paper/main.tex` by the builder, word for word, with
  each version's own numbers for cross-references. Only new options are written.

## Files

- `build_options.py` — builds a document from a rows file (format in its docstring).
- `make_part1.py` — turns drafted layouts (`rows/src/structures.json`) into `rows/part1_structure.json`.
- `make_rows.py` — merges drafted options into `rows/part2_model_levels.json` (from the skeleton, the Simple and
  Medium drafts and the difference lines) and `rows/part3_1_introduction.json` (from the base rows and the new
  options).
- `lint_options.py` — style and real-difference checks.
- `rows/` — the rows files the documents are built from; `rows/src/` — their sources: the base rows with R and O,
  the Part 2 skeleton (the Complex column), and the drafts as checked (layouts, Simple, Medium, introduction
  options, Part 2 difference lines).
- `LEDGER.md` — Stella's decisions round by round: what to keep, drop, or write more of.

## Building

From `pinning/docs/options/`, after compiling `paper/main.tex` and `paper/main_rewrite.tex` (`latexmk -pdf` in
`paper/`), whose `.aux` files give the printed numbers:

```
python3 -B make_part1.py rows/src/structures.json rows/part1_structure.json
python3 -B make_rows.py part2 rows/src/part2_model_levels.skeleton.json rows/src/simple.json rows/src/medium.json rows/src/part2_diffs.json rows/part2_model_levels.json
python3 -B make_rows.py intro rows/src/part3_1_introduction.base.json rows/src/intro.json rows/part3_1_introduction.json
python3 -B build_options.py rows/part2_model_levels.json OUT_DIR --aux-original ../../paper/main.aux --aux-rewrite ../../paper/main_rewrite.aux
python3 -B lint_options.py rows/part2_model_levels.json --aux-original ../../paper/main.aux --aux-rewrite ../../paper/main_rewrite.aux
```

## How a round works

Stella prints the documents and marks them up. Comments come back as photos of the pages or typed against cell
IDs (e.g. "T.1.4: R1, but keep O's last sentence"; "M.17-S: too thin"). Each comment goes into `LEDGER.md`; the
rows are revised (options dropped, rewritten or added) and the documents rebuilt. When every row holds only
options she likes, a clean set with a pick sheet goes to Johan.
