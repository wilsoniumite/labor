# STATE — three-drivers (blog-support thread)

**Project:** data support for the blog post "What do we do if many people aren't working?"
(draft in progress on wilsoniumite.com; follow-up to the 2026-08-10 post). Napkin-grade thread:
lighter than the paper threads, same no-fudging rules.
**State as of:** 2026-08-14 (thread created this session).

## Where things stand

Built in one session, all green:

1. **Seven standing risk/essential-service lists** collected and structured →
   `data/risk_lists.csv` (190 items): NSM-22 16 sectors, NATO 7 baseline requirements,
   Finland 7 vital functions, UK NRR 2025 (88 transcribed; doc says 89 — unresolved, reported),
   MSB NRSB 2025 (26 threats, translated), Lloyd's RDS Jan-2026, WEF GRR 2026 Fig-3 top-10s.
   Source PDFs vendored in `data/raw/`.
2. **Majors→jobs match**: NSCG 2023 Table 1-3 (53.7% closely related / 19.1% not; bachelor's
   25.3% not) + NY Fed outcomes by major (median underemployment 42.9%; Agriculture 57.1%,
   5th worst — the killer fact: even people who study farming mostly can't work in it).
3. **The three-driver napkin** → `data/three_drivers.csv`: market pull (QCEW 2024 wage-bill
   shares, 99.8% coverage), crisis value (list tally, 0-7), people pull (NCES 2021-22 degree
   shares, 16.6% deliberately unmapped). Pattern as hypothesized: water/energy/food/transport
   crisis-high & market-quiet; retail/professional the reverse; health aligned; media & arts
   people-pull excess.
4. **Two figures** (dataviz-skill palette, eyeballed at 200dpi): `fig_drivers_scatter.png`
   (the quadrant chart), `fig_majors_underemployment.png` (24 best/worst majors, essential
   feeders in orange).

Context that produced this thread (chat, 2026-08-14): the "how to estimate true value" discussion —
crisis shadow prices over scenario lists as the estimator; quantity instruments not wage subsidies
(paper's App B/F.1); short universal + long selective rotations; her calls: no engineered prestige
(personal connection instead), no box-ticking oversight (involvement with a real "human slice",
Bainbridge 1983 anchor); blend rule "trust the market in proportion to how much human work is left
in the sector."

## Open / next candidates (not committed)

- Draft the back half of the blog post from the chat synthesis + these figures (her call).
- Sweden-side napkin (SCB wage bills, UKÄ degrees) if she wants a home-market version.
- UK NRR likelihood×impact scores per risk are extractable from the vendored PDF if the napkin
  ever needs severity weights (deliberately skipped — list membership was the deliverable).
- The λ-by-sector series (the-link-revision §10 assembly (2)) doubles as this program's
  allocation key — flagged in chat as the "one measurement, two uses" link to the paper thread.
- Resolve the NRR 88-vs-89 count if it ever matters.

## Standing rules (inherited)

Primary sources; on failure stop and report, never substitute; judgment layers visible in code;
this thread adds: napkin conclusions are patterns, not point estimates — don't quote its numbers
into the paper threads without a proper pass.

## File map

See README.md. Everything reruns from `data/raw/` with zero downloads.
