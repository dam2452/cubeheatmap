"""08 — Dark background theme."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import cubeheatmap as ch

rng = np.random.default_rng(42)
TIMEPOINTS = ["Day14", "Day21", "Day40"]

hm = ch.CubeHeatmap.from_matrix(
    rng.uniform(-5, 5, (12, 3)),
    row_labels=[f"Gene_{i:02d}" for i in range(12)],
    col_labels=TIMEPOINTS,
)

dark = ch.Style(
    cmap="RdBu_r",
    vmin=-5,
    vmax=5,
    fig_facecolor="#1A1A2E",
    ax_facecolor="#1A1A2E",
    row_label_color="#CCCCCC",
    col_label_color="#CCCCCC",
    title_color="#EEEEEE",
    colorbar_label="log2FC",
    colorbar_tick_fontsize=8.0,
    colorbar_fontsize=9.0,
    cell_gap=0.06,
)
ax = ch.draw(hm, title="Dark theme", subtitle="12 genes x 3 timepoints", style=dark)
ax.figure.savefig("example_output/08_dark_theme.png", dpi=150, bbox_inches="tight")
plt.close(ax.figure)
print("-> example_output/08_dark_theme.png")
