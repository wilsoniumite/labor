# Drafted prose in `latex/v6_walls.tex` — for the voice pass (2026-09-02)

Everything below is Claude-drafted, relative to your `v5 (1).tex`. Each item gives
where it sits, what it replaced (if anything), and the new text verbatim, LaTeX
cross-references kept so the round trip loses nothing. Figure captions are here;
the labels inside the figures are in `figure_text_2026-09-02.md`. Nothing else
in the tex changed.

## 1. §3 (Tasks and the assignment margin) — the closed set introduced

Inserted after "(flat stretches are handled in Appendix~\ref{app:environment})."
and before "Competitive assignment then produces a threshold":

> Some tasks no machine can hold at any price: $\gamma_M(x) = 0$ there, relative human productivity is unbounded, and the relabeling places them last. Let $H$ be that set, the tasks closed to machines; Figure~\ref{fig:schedule} draws it as a wall at the right edge of the schedule. Labor holds $H$ at any wage, so the margin below lies among the tasks machines can reach; no wage is set along the wall itself, and Section~\ref{sec:interval} says what sets it there. The flat limit of Section~\ref{sec:limit} is the case in which $H$ has emptied; Appendix~\ref{app:human} keeps it.

## 2. Figure 1 caption — one new sentence

Full caption, the new sentence marked:

> The task-assignment margin. Tasks are ordered so $\gamma(x)$ increases; the ratio $w/c$ divides them: machines hold every task with $\gamma(x)<w/c$, labor holds every task above, and at $x^*$ the two inputs cost the same. **[new]** The tasks closed to machines, the set $H$, sit at the right edge as a wall: no machine holds them at any price, labor holds them at any wage, and no wage is set along the wall itself (Section~\ref{sec:interval}). **[end new]** A cheaper machine or a lower $\gamma$ near the margin shifts tasks toward machines. The two automation channels developed below operate through these objects: task automation changes relative capability at the assignment margin, while recursive automation changes the price of the machine substitute itself.

## 3. §2 (The classical accounts) — one clause

Was: "Section~\ref{sec:history} reads the classical case as the flat configuration of the schedule built below."

> Section~\ref{sec:history} reads the classical case as the configuration of the schedule built below in which nearly every task is closed to machines.

## 4. §6 (The two sides of the wage) — two new paragraphs after "Heterogeneity"

No mathematics, by design.

> **What sets the wage at the wall.** The ceiling above is a machine price: at the marginal task the worker is paid what the machine would cost there, scaled by how much better the human is at it. On a task closed to machines there is no such price. No machine does the task at any cost, so nothing about the task itself says what an hour of it is worth, and the wage there is set elsewhere. If the worker still holds some task machines can reach, the machine sets the wage at that task and the closed tasks are simply done at it. If every task the worker holds is closed, the wage is a scarcity price: the worker's hours against the demand for what only those hours can make, with no machine in the comparison. That is how every wage was set before machines reached anything, and the floor above is what it settled to.

> **Other people supply the substitute the machine cannot.** A trained worker and an untrained one can both do most tasks, at different levels, so the two are ranked against each other task by task exactly as labor is ranked against machines, and the ratio of their wages is set where that ranking is cut: the trained worker holds the tasks where the advantage over the untrained is largest, the untrained the rest, and more trained workers push the cut toward tasks where the advantage is smaller. Comparative advantage between people therefore sets the premium, not the level. The level under the whole structure is whichever base the machine leaves standing: the ceiling at the untrained worker's marginal task while machines still contest one, or the floor when they contest none. Training is a produced part of a person, bought with years, so in the long run its premium recovers those years and exceeds them only while trained hours are short. Section~\ref{sec:history} reads history along these lines, and Appendix~\ref{app:human} keeps the closed set in the limit.

## 5. §8 title and opening

Title: "History as three configurations of the model" became "History as four configurations of the model" (a count change to a title you retyped today; revert on your word).

Opening paragraph, the second sentence is new:

> The model can be applied to the long record as four configurations of the relative-productivity schedule (Figure~\ref{fig:eras}). Because the schedule is a person's (Section~\ref{sec:interval}), the figure draws each configuration twice: for a young entrant with no training, and for a worker with years of training or experience.

## 6. Figure 2 caption — entirely new

> Four configurations of the schedule (schematic), for a young entrant with no training (top) and a worker with years of training or experience (bottom). Tasks closed to machines sit at the right edge as a wall, and the dot marks each era's margin; a dot on the wall marks a wage no machine sets (Section~\ref{sec:interval}). Pre-industrial: nearly every task is closed for both, and both margins sit at the wall. Industrial: physical tasks open; the entrant's margin sits on a steep stretch while the trained worker's stays at the wall. Computing: routine tasks open; the entrant's margin sits on a flat stretch while the trained worker's still stays at the wall. AI: the wall retreats for both, and both margins sit on the same flat stretch.

## 7. §8 pre-industrial paragraph

Was: "With machines scarcely present, nearly every task is a labor task; the schedule is compressed and the binding boundary of the wage interval is the lower one, which is a land price."

> With machines scarcely present, nearly every task is closed to them; the margin sits at the wall for entrant and master alike, so the machine prices no one's hour, the case Section~\ref{sec:interval} describes, and the binding boundary of the wage interval is the lower one, which is a land price.

Appended at the end of the paragraph, after "The classical account is one configuration of our model.":

> The entrant is the farm servant hired by the year; the trained worker is the craftsman after a seven-year apprenticeship, whose premium over the servant is the cost of those years, recovered.

## 8. §8 industrial paragraph

Inserted after "The schedule became enormously dispersed and steep." and before your "That dispersion opened high-productivity tasks to labor" (so that back-reference now reaches across the insertion; move the two sentences later if you prefer):

> It did so for the entrant first: the young mill hand or hand-loom weaver held the tasks engines were reaching one by one, and the margin sat on the steep stretch, where what the engine cost at the next task priced the hour. The trained worker, the millwright, the engineer, the clerk, held tasks closed to engines; that margin stayed at the wall, so no machine set the wage, and it was instead the scarcity price Section~\ref{sec:interval} describes, on trained hands and heads, kept scarce by the years the training took.

## 9. §8 post-industrial paragraph

Inserted after "(Autor and Dorn 2013) are the cross-sectional trace.":

> The entrant is the young clerk, cashier, or assembler whose routine tasks software and machines reached at similar cost: the margin sat on a flat stretch and the wage was pinned there. The trained worker, the developer, the physician, the engineer, held tasks computers could not: the margin stayed at the wall, and the premium for training was what the period's expansion of higher education chased.

Inserted after your "$\lambda$, the labor inside the machine sector itself." and before "Section~\ref{sec:ai} takes this up":

> It is also the first flattening to reach the trained worker's wall: the schedule flattens to the same stretch for both, and the premium for training decays as the trained stock stops being scarce.

## 10. Appendix A, first paragraph — one phrase

Was: "one machine type, no reserved tasks, no government"

> one machine type, no tasks closed to machines by preference or law, no government

## Flags, not edits

- Your own text, §5: "adds approximately nothing of anything. so its competitive price is approximately zero." — a period before a lowercase "so".
- The Figure 3 caption still describes the old two-series 1964-base figure; the artwork is now the four-category fan on a 1950 base.
