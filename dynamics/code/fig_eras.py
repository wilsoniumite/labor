# fig_eras.py — schematic: the relative-productivity schedule across three
# technological eras, in the rewrite's register (no coined vocabulary).
# Pure schematic, no data; regenerates link-repo fig2_arcs.png with the
# y-axis relabeled from "effective human edge" to "relative human
# productivity" and a neutral annotation.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["font.size"] = 11

x = np.linspace(0, 1, 400)

industrial = 0.3 + 8.0 * x**2.6          # dispersed, steep
computing  = 0.9 + 5.5 * x**2.2          # flattened at the simple end
ai         = 0.85 + 1.2 * x**1.8         # flattening becomes general

fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=150)
ax.plot(x, industrial, color="#1a1a3d", lw=2.4,
        label="industrial era: dispersed, steep")
ax.plot(x, computing, color="#4878b8", lw=2.4,
        label="computing: flattened at the simple end")
ax.plot(x, ai, color="#8b2020", lw=2.4,
        label="AI: flattening becomes general")

ax.annotate("the level at the marginal task falls,\nand the slope falls with it",
            xy=(0.84, 0.45), fontsize=10, color="#8b2020", ha="center")

ax.set_xlabel("tasks x")
ax.set_ylabel("relative human productivity γ(x)")
ax.set_xlim(-0.02, 1.04)
ax.set_ylim(0, 8.6)
ax.grid(alpha=0.25, lw=0.5)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper left", framealpha=0.95, fontsize=9.5)

fig.tight_layout()
fig.savefig("figures/fig_eras.png", bbox_inches="tight")
print("wrote figures/fig_eras.png")
