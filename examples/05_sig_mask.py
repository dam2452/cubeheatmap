"""05 — Significance markers with sig_mask."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import cubeheatmap as ch

rng = np.random.default_rng(42)
TIMEPOINTS = ["Day14", "Day21", "Day40"]

mat = rng.uniform(-4, 4, (10, 3))
mask = np.abs(mat) > 2.5

hm = ch.CubeHeatmap.from_matrix(
    mat,
    row_labels=[f"Gene_{i}" for i in range(10)],
    col_labels=TIMEPOINTS,
)

style = ch.Style(
    cmap="RdBu_r",
    vmin=-4,
    vmax=4,
    colorbar_label="log2FC",
    sig_marker="*",
    sig_marker_fontsize=9.0,
)
ax = ch.draw(hm, title="With significance markers", style=style, sig_mask=mask)
ax.figure.savefig("example_output/05_sig_mask.png", dpi=150, bbox_inches="tight")
plt.close(ax.figure)
print("-> example_output/05_sig_mask.png")
