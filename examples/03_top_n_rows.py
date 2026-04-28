"""03 — top_n_rows() automatic row selection."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import cubeheatmap as ch

rng = np.random.default_rng(42)
TIMEPOINTS = ["Day14", "Day21", "Day40"]

big_matrix = rng.uniform(-6, 6, (60, 3))
hm_big = ch.CubeHeatmap.from_matrix(
    big_matrix,
    row_labels=[f"Gene_{i:02d}" for i in range(60)],
    col_labels=TIMEPOINTS,
)

hm = hm_big.top_n_rows(20)

style = ch.Style(
    cmap="RdBu_r",
    vmin=-6,
    vmax=6,
    colorbar_label="log2FC",
    row_label_fontsize=8.0,
    cell_size=0.5,
)
ax = ch.draw(hm, title="Top 20 genes (max |LFC|)", style=style)
ax.figure.savefig("example_output/03_top_n_rows.png", dpi=150, bbox_inches="tight")
plt.close(ax.figure)
print("-> example_output/03_top_n_rows.png")
