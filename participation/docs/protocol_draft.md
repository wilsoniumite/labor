# Participation — protocol draft (theory side, written before any data values were seen)

Draft of 2026-10-08. Becomes `PROTOCOL.md` once data codes are fixed; then frozen by commit before any
value is downloaded into this folder.

## The design: guided by data, tested against something

Three tiers, one rule each.

1. **P — the model's predictions, stated now.** Derived from `pinning/paper/main.tex` (Section 7 the outside
   option, Appendix B household participation, the eras section, Appendix conditionality). Each with a measure,
   one primary specification, a sign, and what would count against it. Never re-specified after data; a variant
   is labelled exploratory.
2. **E — what the data suggest.** Countries are split once, by a seeded draw within regions, into an EXPLORE half
   and a CONFIRM half. Anything goes on the explore half. What it suggests is written down as E-hypotheses with
   exact specifications and frozen by commit.
3. **The one look.** After the E freeze, P and E are tested once on the confirm half (the code refuses to load
   confirm countries before the freeze commit exists). Everything is reported, nulls included. The full sample
   is reported second.

## The model's objects for a group g (sex x age x schooling)

- wage: `w_g = c(r) gamma(x*_g)` on the contestable stretch, a scarcity price at the wall;
- exit value `s_g(q) = max(s0_g - q h_e, s_under_g)`, `q = r/p` (non-produced services relative to goods);
- non-labour income `A_g` (Appendix B: work iff `chi <= log(1 + v/A)`; A is ownership income after housing);
- transfers in and out of work (`m_w`, `m_e`).

Key derivation (to be checked): with housing needed in work and in exit and concave utility (App. B log), the
sign of d(participation)/dq is minus the sign of the group's NET housing position. Net short (renters, people
who will need to buy): q up -> poorer after housing -> work more (enclosure). Net long (outright owners holding
more than they will consume, who can downsize or bequeath): q up -> richer -> work less. Exactly hedged
(own what they occupy, no plans to sell): no flow effect. Dependants (host pays housing): s at the flat
segment, no direct effect; the host's budget carries it.

## Draft predictions

Distinctive = the model says something a standard labour-supply model does not commit to.

- **P1 (distinctive) — the tenure split.** A rise in q raises participation of young adults (25-34, net short)
  and lowers or leaves unchanged that of older adults (55-64, net long). Primary: beta_young - beta_old > 0.
- **P2 — coresidence absorbs q for the young.** The share of 25-34-year-olds living with parents rises with q
  (rent relative to the young's wage), holding youth unemployment.
- **P3 (distinctive) — the second earner is enclosed.** Prime-age (25-54) women's participation rises with q,
  more than men's: beta_W > 0 and beta_W > beta_M.
- **P4 (distinctive) — where the dependency floor is available, youth non-employment is exit, not search.**
  Among young people not in employment, the inactive (not seeking, not in education) share rises with the
  coresidence share. A search reading (parents finance longer search) predicts the opposite sign.
- **P5 — entrants first.** Since generative AI (2023-), employment of 20-24 falls relative to 25-54 more where
  the pre-2023 employment share in AI-exposed (clerical) occupations was higher.
- **P6 — aging pulls the margin.** Faster population aging goes with a faster fall in the employment share of
  automatable (routine) occupations.
- **P7 — public provision of exit.** Higher out-of-work replacement for older people (pension net replacement,
  earlier statutory ages) lowers 60-64 participation. Consistency check, not distinctive.
- **P8 — schooling as paid exit.** Enrolment of 20-24 rises when youth labour prospects fall (youth
  unemployment). Consistency check, not distinctive.

## Not testable yet (stated so they are not forgotten)

- The hump: along an automation path each group's participation first rises (s falling, enclosure) then falls
  (w reaching the dependency floor), entrants first. Needs a longer AI period.
- Goods-rich, space-poor exit: cheap entertainment raises the exit value at the dependency floor
  (young men at home). Needs time use or micro data.
