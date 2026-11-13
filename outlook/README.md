# outlook — the case, and the model behind watch.wilsoniumite.com

What we think is happening as AI takes over paid work, stated so that data can confirm or contradict it, with one run
of a model that puts numbers on it. Set on **13 November 2026** from a clean slate. `STATE.md` is the session entry
point; this file is the case itself.

## The case in one paragraph

AI is making machine work cheap and everything it cannot produce dear. Its first effects are a squeeze, not a loss
of jobs: on the pay and hiring of people entering office work, on pay's share of income, and on capital, power and
sites, which the build-out has made scarce. That squeeze, with money already dear, is bringing a downturn about the
size of 2001's. The downturn is when the loss of jobs shows, because the office jobs cut in it are not all refilled.
After it, AI's pace picks up, and how far the damage goes is decided by the public response.

## The seven points

Each is a claim the evidence can move. The numbers are the case's run (`results/outlook.json`); "counts against" is
what would make us drop the point.

**Now: the squeeze (2026–27)**

1. **AI can already do much office work, and its price is falling.** Measured capability on whole tasks keeps rising
   and the price of a given capability keeps falling. *Counts against:* a year without progress on benchmarks of whole
   tasks, or prices per task that stop falling.
2. **Firms use it first to hire fewer people and to thin office layers. The loss of jobs is small and growing.** On
   the US jobs data since the employment peak of September 2024, AI's net displacement is at most 0.2 points of the
   workforce a year (the trend itself is not distinguishable from zero). The case has it double every two years:
   0.3 points a year by late 2027, 0.4 by late 2028, 0.9 by late 2030. People entering office work are hit first.
   *Counts against:* office jobs growing in line with other jobs, graduates' unemployment falling back against
   others', employment among 25–54-year-olds recovering.
3. **Income is moving from pay to owners.** Labour's share of US business output is the lowest since 1947 while
   output per hour grows faster than pay. It moves through pay first and through jobs later. *Counts against:* the
   share recovering outside a recession.
4. **Capital, power and sites are scarce, so borrowing stays dear.** The build-out costs more than its builders earn
   and is financed at long-term interest rates that are the highest in two decades, while grid connections, sites and
   permits ration what can be built. In the run the Federal Reserve raises its rate a little further, to 4.1% in early
   2027. *Counts against:* long-term real interest rates falling back while the build-out speeds up, or its weaker
   borrowers funding themselves freely again.

**Next: the downturn (2027–29)**

5. **Dear money and a retreat from AI's weaker borrowers bring a downturn about the size of 2001's.** Share prices
   lose half as much as in the dot-com crash, on that crash's path from their high of 6 October 2026 (US households'
   shares 22% down at the bottom). US unemployment rises from 4.2% to 5.2% by the end of 2027 and 6.2% in early 2029;
   the Sahm rule triggers in July 2027; the four economies' output is 2.3% below capacity at worst. The Federal
   Reserve cuts from mid-2027, to 2.7% by the end of 2028. *Counts against:* no rise in unemployment by the end of
   2027, or a fall in shares and credit that reverses with the build-out funded from its builders' own cash.
6. **The jobs cut in it do not all come back.** Firms automate part of what they cut. In the run the response
   arrives late (from April 2029 in the United States, once unemployment has risen two points) and brings
   unemployment back to 4.7% by late 2030, but the share of people out of work never returns to where it started.
   *Counts against:* office employment back at its level before the downturn within two years of its low.

**Later: cheap machine work (2029–32)**

7. **After it, AI's pace picks up, and the response decides how far it goes.** In the run the share of the US
   workforce out of work is 8.6% by mid-2032 and still rising (7.4% unemployed, 1.1% out of the workforce), and the
   Federal Reserve's rate is below 2%. If the pace stayed as slow as it has been: 5.8%. If it doubled every year:
   10.1%. With spending cuts, tariffs and no bank rescues: 17.7%, with output 17% below capacity; with a
   dot-com-sized bust as well, a depression. With an income guarantee: 7.9%. *Counts against:* a pace still at
   today's bound in 2029.

## What the case does not claim

- **A date for the long run.** The paper's limiting results (wages pinned by replacement cost, rents taking the
  income) are where the mechanism points, not a path with years on it. Calibration (c) of `paths/`, which put years
  on it, overstates site rent by a factor of two to four (`pinning/STATE.md`, 3 November 2026) and is not used here.
- **Numbers for Europe.** The engine has no exchange rates and reads any shortfall of prices from their targeted
  path as heavier debt, so it overstates the damage where inflation runs a little under target (France, Sweden). The
  run's numbers for them are on the model's page with that limit; the case is stated for the United States.
- **That the engine returns to where it started.** With no bust and no AI job losses US unemployment still drifts
  from 4.2% to 4.7% by 2032 (check R8): a small early gap is never fully closed. Readings far out lean on the
  assumed pace and on this.
- **A return of the 1970s.** The case has inflation fading while unemployment rises. It holds that because pay is
  not chasing prices (labour's share is falling), the downturn comes from lost spending, scarce power and sites move
  some prices against others, and expected inflation has stayed near target. It is an assumption, and the main way
  the squeeze could go further than the case has it. If core inflation stays where it started, 9.1% of the US
  workforce is out of work by mid-2032 (the case: 8.6%). With a second wave of three points through 2028 the Federal
  Reserve's rate reaches 7.3% and 9.6% are out of work; with expectations half following inflation, 10.3% and 10.2%;
  with expectations following it as in the 1970s, 19% and 12.3% (check R10). *What would show it:* core inflation
  still near 3% in mid-2027 while unemployment rises; inflation expected five to ten years ahead leaving 1.5–3%; real
  pay per hour outgrowing output per hour. The engine counts no harm from inflation itself, only from the policy
  rate's answer to it: these runs price the fight against a second wave, not the cost of letting one run (with rates
  held through the same wave the engine shows fewer out of work, which is its blind spot, not a finding).

## The model

`code/outlook.py` runs the crash engine of `paths/code/global_crash.py` — five economies by month, fitted on nine
past downturns and checked on the dot-com bust it was not fitted on — unchanged, and adds only inputs, each measured
or stated:

| input | value | from |
|---|---|---|
| the start | the economies in September 2026 | the dated vintage, `paths/cache/start` |
| inflation above target at the start | fades with a half-life of 1.8 years (US), 1.0 (euro area) | each region's own core inflation, peak to low, on the vintage |
| the pace now | 0.218 points of the US workforce a year | `paths/results/pace.json`: the trend since the 2024 employment peak plus two standard errors |
| how it grows | doubles every two years, up to a point a year | stated |
| who leaves the workforce | 59% of the displaced (US) | the middle of the three bases it is measured from |
| the bust | half the dot-com bust, on its measured path, from 6 October 2026 | stated size; measured path and date |
| robots | not within the run | stated |
| policy | today's rules; each lever starts once unemployment there has risen by its trigger in the run | the engine's rules |

Three additions to the engine's code, each off at its default (check E1 and the engine's own 85 checks: without
them the engine is the stored one, bit for bit): `Shock.push`, an inflation input; `Rules.support_level`, the level
of unemployment benefits against today's; `Rules.guarantee_finance`, how an income guarantee is paid for (borrowing,
a tax on wages or a levy on the income AI moves to owners: the sources a care build-out already had, shared with it).

### The response, policy by policy

A run's response is set switch by switch (`SWITCHES`, `TODAY`); the engine's presets are bundles of them (`BUNDLES`,
reproduced rule for rule: check L1), and a run is named by the bundle its switches are nearest to (`nearest`), so one
response has one name. A switch that does nothing in a run (a guarantee's share without a guarantee) is put back to
today's (`settle`).

| switch | options or range | today |
|---|---|---|
| `rates` | `rule` (Taylor), `hold` (where they stood at the start), `gold` (no reflation) | rule |
| `expect` | `anchored` (0.9 on the target), `slipping` (0.6), `loose` (0.2, the 1930s' and the 1970s') | anchored |
| `prices` | `sticky`, `free` (1929–33's slope) | sticky |
| `insured`, `rescues` | `on`, `off` | on |
| `benefits` | 0–1.5 times today's replacement rate | 1 |
| `response` | `none`, `stimulus`, `guarantee`, `cuts`, from a rise of `trigger` (0.5–4 points); a guarantee replaces `share` (0.5–1) of lost pay | stimulus, 2 points |
| `tariff` | 0–30 points, raised `tariff_by` `all` or `us` (the US, and on its exports in return), `tariff_from` April 2027, 2028 or 2029 | 0 |
| `care` | `trend`, `cut`, `expand` at `care_pace` (0.5–2 points of employment a year) | trend |
| `paid` | how a guarantee or a build-out is paid for: `borrowing`, `wages`, `levy` (which takes `levy`, 0.25–1, of the pay AI displaced) | borrowing |

One switch at a time on the case (US share out of work in mid-2032; the case 8.6%): central banks hold their rates
9.3%; expectations slipping 9.1%; no deposit insurance 13.1%; no benefits 10.4%, half as high again 7.9%; no response
9.5%; spending cuts 10.2%; a response after one point 8.3%; an income guarantee borrowed 7.9%, by a levy 7.9%, by a
tax on wages 8.7% (worse than none: those still in work spend less; check L4); tariffs of 20 points by everyone 10.5%,
by the US 9.9%; care stops hiring 9.4%; care built out 7.4%, by a tax on wages 7.5%. Benefits and the stimulus are
charged to no budget in the engine; a land or rent tax is not in it.

### Inflation

`inflation` is a setting: `fades` (the case: each region's excess at its measured half-life), `stays` (the excess at
the start does not fade), `wave` (stated: three points more core inflation a year in every economy, building through
2027, held through 2028, gone by 2030).

```
python code/outlook.py            # writes results/outlook.json (under a minute)
python checks/check_outlook.py    # 25 checks: the engine untouched, the inputs as measured, the findings as found
```

The watcher (`wilsoniumite/watch`) exports this model to the website, runs the same engine in the page, and holds
the dated predictions that test the seven points.
