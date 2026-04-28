"""07 — Rounded cell corners."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import cubeheatmap as ch

rng = np.random.default_rng(42)
TIMEPOINTS = ["Day14", "Day21", "Day40"]

hm = ch.CubeHeatmap.from_matrix(
    rng.uniform(-3, 3, (8, 3)),
    row_labels=[f"Gene_{i}" for i in range(8)],
    col_labels=TIMEPOINTS,
)

style = ch.Style(
    cmap="RdBu_r",
    vmin=-3,
    vmax=3,
    cell_rounding=0.15,
    cell_gap=0.10,
    colorbar_label="LFC",
)
ax = ch.draw(hm, title="Rounded corners", style=style)
ax.figure.savefig("example_output/07_rounded.png", dpi=150, bbox_inches="tight")
plt.close(ax.figure)
print("-> example_output/07_rounded.png")
