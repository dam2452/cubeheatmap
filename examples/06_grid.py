"""06 — draw_grid() multi-panel layout."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import cubeheatmap as ch

rng = np.random.default_rng(42)
TIMEPOINTS = ["Day14", "Day21", "Day40"]
cell_types = ["T cell", "B cell", "NK cell", "Macrophage"]

heatmaps = [
    ch.CubeHeatmap.from_matrix(
        rng.uniform(-4, 4, (8, len(TIMEPOINTS))),
        row_labels=[f"Gene_{i}" for i in range(8)],
        col_labels=TIMEPOINTS,
    )
    for _ in cell_types
]

style = ch.Style(
    cmap="RdBu_r",
    vmin=-4,
    vmax=4,
    colorbar_label="log2FC",
    cell_size=0.45,
    cell_gap=0.04,
    row_label_fontsize=7.5,
)

fig = ch.draw_grid(
    heatmaps,
    titles=cell_types,
    suptitle="DEG LFC Heatmaps per cell type",
    ncols=2,
    style=style,
)
fig.savefig("example_output/06_grid.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print("-> example_output/06_grid.png")
