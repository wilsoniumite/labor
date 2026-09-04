# STATE — resume point for the next session

**Project:** The Long Record — fitting the model's three-configuration reading
of the seven-century wage record (working title *One Schedule, Seven
Centuries*). Spun out of `../the-link-revision/` on 2026-08-17; the paper
(`../the-link-revision/paper/pinning.html`) is untouched by this thread.
**Collaboration:** same contract as the parent thread — working format,
sequencing, and drafting delegated to Claude; direct critique preferred;
Stella's standing rules apply in full (see spec §4.7).
**State as of:** 2026-08-17 (founding session).

## Where things stand

**Phase 0 is DONE; the thread is parked at BREAKPOINT A, which is Stella's.**
The governing document is `docs/spec.md` — why, considerations, identification
map, and the phased plan (sparser as it goes, breakpoints A–C as zoom-outs,
B is the kill point). Read it before anything else.

Founding-session results, in one place:

1. **The regime checks ran ALL GREEN (12)** —
   `checks/check_longrecord_regimes.py`. Substantive outcome: the founding
   discussion's headline claim (a sign flip in wage–rent comovement at the
   regime switch) is **REFUTED** as originally stated — nominal comovement is
   numeraire content (homogeneity, R3), and the wage's population-response is
   negative in both regimes (R4). The surviving discriminators, now the
   thread's spine: **D1** q's determinant flips (scarcity-side N/T in the
   floor regime; cost-side machine recipe in the flat limit — R2e; the
   transition-path version is OPEN ALGEBRA, queued for Phase 2's check pass);
   **D2** the joint switch date (wage escape = land-share exit, estimated
   independently, must agree); **D3** floor-era welfare-ratio variance
   explained by (N, T) with h_e consistent with the historical plot-size
   literature. Fits in this thread run on deflated objects only (welfare
   ratio, w/r, q) — nominal-comovement tests are banned by R3.
2. **Source inventory probed** (spec §7): BoE millennium set reachable
   directly; Clark's UC Davis pages reachable via the harness fetcher only
   (local curl blocked for that host); BNS same route, replication archive
   still to locate; **Allen's site BLOCKED (403)** from both routes —
   alternates listed in the spec, to try at Phase 1, reported not
   substituted.
3. **No data pulled, deliberately** — Phase 1 is gated on Breakpoint A.

## Verify-list — 2026-08-17: the founding unit (veto window, current)

- [ ] The spec's framing: the thread exists to validate §9 by fitting, tease
      out (φ, h_e, s₀−s_d, slope path), and run the D2 joint-date test;
      England-only spine as default scope.
- [ ] The correction stands as recorded: the sign-flip prize from the founding
      discussion narrowed to D1–D3 under the Phase-0 check. If this narrowing
      changes her go/no-go, that is exactly what Breakpoint A is for.
- [ ] The extension's shape: three slow states (population φ, idle-margin
      path, capped piecewise tech path) over the unchanged static core;
      decadal frequency + annual Black Death window as default.
- [ ] The plan's breakpoints: A (before any data), B (eyeball test = kill
      point, tech-knot freeze), C (magnitudes/novelty vs BNS). Phases 3–4
      deliberately sparse until C.
- [ ] New-parameter budget as stated (~10–12 total incl. ≤ 6 tech knots).

## Next actions (priority order)

0. **Breakpoint A (Stella):** the five questions in spec §6, answered in
   writing here. Nothing else proceeds first.
1. **Phase 1 on her go:** pull order BoE → Clark → BNS → Allen-alternates;
   validation pass; decadal panel; the descriptive seven-century sheet;
   `data/DATA_NOTES.md` in house format.
2. **Queued check pass (Phase 2 gate):** sloped-era q-determination (D1's
   open half) + floor-block comparative statics, sympy + numeric, before any
   fitting.

## File map

```
long-record/
├── STATE.md                              ← you are here; start here next session
├── docs/
│   └── spec.md                           the governing spec: why, risks, plan, breakpoints
├── checks/
│   └── check_longrecord_regimes.py       Phase-0 regime algebra, ALL GREEN (12); refutation record
└── (data/, code/, figures/ created at Phase 1, not before)
```

## Repro notes

- Checks: `./venv/Scripts/python.exe long-record/checks/check_longrecord_regimes.py`
  from the repo root (shared venv; python 3.13, sympy + numpy).
- Network quirk of this machine: curl is blocked for several academic hosts
  (UC Davis, NBER, robert-c-allen.net) while the harness fetcher gets
  through, and bankofengland.co.uk is open to both. Recorded in spec §7;
  matters for Phase 1's pull scripts (they may need the fetcher route or a
  vendored-download step, documented when built).
