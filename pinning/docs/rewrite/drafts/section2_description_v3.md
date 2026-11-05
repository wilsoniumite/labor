# Section 2, rewritten as a description of the economy (draft v3, 2026-11-05)

v3 (Stella): only the task model and the cost recursion get citations: Zeira (1998) and Acemoglu and Restrepo (2018) for the tasks; Leontief (1936) and Sraffa (1960) for the price system. Lewis, Ricardo and George were tried in v2 and taken out. Acemoglu and Restrepo's own text (NBER WP 22252) says that "Zeira's model is a special case of our framework". Earlier versions: section2_description_v1.md and _v2.md.

This follows Lucas (1978), whose Section 2 is "Description of the economy" (informal: the consumer
and what he maximizes, the productive units, ownership, then what is easy and what is hard), and
whose Section 3, "Definition of equilibrium", opens: "The economy described in the preceding
section is specified by the functions U and F and the number beta."

Structure:
- **§2 Description of the economy** (new, below).
- **§3 Definition of equilibrium.** It opens with the primitives sentence in Lucas's form, followed
  by Assumptions 1–5, the cost system, the government, Definition 1 (with c_o > 0), Definitions 2–3
  and the AI paragraph. All of this is from synthesis.md §2.1.
- **§4 onward.** The results, renumbered by one.

Tags: [NEW] new text; [HERS] the authors' text, verbatim (main.tex line 268).

---

\section{Description of the economy}

[NEW]
Consider an economy with two kinds of households, workers and an owner, competitive firms, and a
government. Time is discrete, and we study stationary equilibria, in which prices and quantities
are the same in every period.

[NEW]
There are $N$ workers. Each has one hour a period, which it can sell at the wage or keep, and
consumes baskets, each made of a unit of a final good and a fixed amount of living space. Selling
the hour costs a worker something, the value of the time and effort it gives up, and this cost
differs from worker to worker. Each worker receives one basket a period as support, whether or not
it works, and spends its wage on further baskets. It works if the baskets an hour buys are worth
more to it than the hour.

[NEW, with HERS line 268 as the fourth sentence]
The owner does not work. It owns the economy's land and its machines, rents both out, provides each
worker's basket of support, and consumes what is left. It stands for whoever sustains a person
outside paid work. For example, an adult may live with parents who provide housing and basic
consumption while the adult decides whether to take paid work. The owner lives forever and
discounts the future, so a machine must earn a return to be worth holding.

[NEW]
Firms make the final good by performing a continuum of tasks, as in the task model of Zeira (1998)
and Acemoglu and Restrepo (2018). Any task open to machines can be done
by an hour of labor or by machine-hours, and firms use whichever is cheaper. Relative to people,
machines are better at some tasks than at others, and some tasks are closed to them, by capability
or by rule. Machines are themselves produced, from machine-hours, labor, and land. Living space is
land as well. Land is the economy's one non-produced input: nothing the economy does adds to it,
and it stands for sites, mineral deposits, and other inputs in fixed supply.

[NEW]
The government can tax land rents and wages and pay transfers. In the baseline it does nothing;
Section 6 uses its instruments.

[NEW, the "easy and hard" paragraph, moved here from the head of the results section, as in Lucas]
In this economy, prices are easy to determine once the wage and the rent on land are known. Each
good's price equals its cost, and tracing costs through the machines that build machines resolves
every price into hours and land, as in the input--output price systems of Leontief (1936) and
Sraffa (1960). The main analytical issue is the wage relative to the rent. It is
set at the marginal task, against a machine whose own price contains wages; by workers who compare
the wage with the cost of a basket that the same costs determine; and by a labor market that the
fixed supply of land closes.

\section{Definition of equilibrium}

[NEW, the primitives sentence in Lucas's form]
The economy described in the preceding section is specified by the relative-productivity schedule
$\gamma$ and its wall $x_H$; the recipe $(a,\lambda,b)$ for building a machine and the machine's
depreciation rate $\delta$; the land $T$; the number of workers $N$, the space $h$ in a basket, and
the distribution $F$ of the costs of work; the owner's discount factor $\beta$ and utility $u$; and
the policy $(\tau_R,\tau_w,d,g_w,g_e,\sigma)$.

[then synthesis.md §2.1 from "\subsection{Tasks, machines, and land}" on, with Definition 1
requiring $c_o>0$]

---

Model checks for the description, against synthesis.md §2.1:
- One indivisible hour, sold or kept: Assumption 4.
- The basket is one unit of the final good and h of space: eq. (7).
- The cost of work chi differs across workers: Assumption 4.
- One basket of support in work and in exit, with the wage spent on more: eq. (budget).
- A worker works iff log(1 + w/P_s) > chi: eq. (8).
- The owner owns the land and the machines, supports the workers and consumes the rest:
  Assumption 5 and eq. (ownerbudget).
- Discounting and the return on machines: rho = 1/beta − 1 and the user cost.
- Tasks open to machines go to the cheaper input; closed tasks go to labor: Assumption 1 and
  Definition 1(i).
- Machines are built from a machine-hours, lambda hours and b land: Assumption 2.
- Space is land services, and land is fixed: Assumption 3.
- The government is inactive in the baseline: §2.5 of the synthesis.
- The easy-and-hard paragraph is synthesis.md line 626, in plain words.
