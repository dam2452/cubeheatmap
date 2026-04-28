"""16 — Dense microarray-style heatmap with tiny cells."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import cubeheatmap as ch

rng = np.random.default_rng(42)

genes = [f"Gene_{i:03d}" for i in range(80)]
conditions = ["Ctrl", "Treat_1h", "Treat_4h", "Treat_12h", "Treat_24h",
              "Treat_48h", "Treat_72h", "Recovery"]

matrix = rng.uniform(-3, 3, (len(genes), len(conditions)))
hm = ch.CubeHeatmap.from_matrix(matrix, row_labels=genes, col_labels=conditions)

style = ch.Style(
    cmap="RdBu_r",
    vmin=-3,
    vmax=3,
    colorbar_label="log2FC",
    cell_size=0.08,
    cell_gap=0.01,
    row_label_fontsize=5.5,
    col_label_fontsize=4.5,
    col_label_rotation=90.0,
    title_fontsize=10.0,
    colorbar_fontsize=7.0,
    colorbar_tick_fontsize=6.5,
    grid_row_label_width=1.2,
    grid_title_height=0.5,
    grid_col_label_height=0.6,
)

ax = ch.draw(hm, title="Dense Microarray-style Heatmap", subtitle="80 genes x 8 conditions", style=style)
ax.figure.savefig("example_output/16_dense_microarray.png", dpi=200, bbox_inches="tight")
plt.close(ax.figure)
print("-> example_output/16_dense_microarray.png")
