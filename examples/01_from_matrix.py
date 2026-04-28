"""01 — Basic from_matrix() usage."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import cubeheatmap as ch

GENES = [
    "Il1b", "Tnf", "Cxcl10", "Ccr2", "S100a8", "Nos2",
    "Arg1", "Trem2", "Spp1", "Mrc1",
    "Lyve1", "Timd4", "Folr2", "Cd163", "Gpnmb",
]
TIMEPOINTS = ["Day14", "Day21", "Day40"]

rng = np.random.default_rng(42)
matrix = rng.uniform(-4, 4, (len(GENES), len(TIMEPOINTS)))

hm = ch.CubeHeatmap.from_matrix(matrix, row_labels=GENES, col_labels=TIMEPOINTS)

style = ch.Style(
    cmap="RdBu_r",
    vmin=-4.0,
    vmax=4.0,
    colorbar_label="log2FC",
    cell_size=0.55,
    cell_gap=0.05,
)
ax = ch.draw(
    hm,
    title="Macrophage DEG",
    subtitle="Day14 / Day21 / Day40 vs Day0",
    style=style,
)
ax.figure.savefig("example_output/01_from_matrix.png", dpi=150, bbox_inches="tight")
plt.close(ax.figure)
print("-> example_output/01_from_matrix.png")
