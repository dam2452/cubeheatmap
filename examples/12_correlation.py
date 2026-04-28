"""12 — Feature correlation matrix."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import cubeheatmap as ch

features = ["Age", "Income", "Score", "Hours", "Rating", "Tenure"]
n = len(features)
rng = np.random.default_rng(7)

A = rng.standard_normal((n, n))
corr = np.corrcoef(A)
corr = (corr + corr.T) / 2
np.fill_diagonal(corr, 1.0)

hm = ch.CubeHeatmap.from_matrix(corr, row_labels=features, col_labels=features)

style = ch.Style(
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    colorbar_label="Pearson r",
    cell_size=0.85,
    cell_gap=0.06,
    annotate=True,
    annotate_fmt="{:.2f}",
    annotate_fontsize=8.0,
    col_label_rotation=30.0,
    cell_rounding=0.12,
)
ax = ch.draw(hm, title="Feature Correlation Matrix", style=style)
ax.figure.savefig("example_output/12_correlation.png", dpi=150, bbox_inches="tight")
plt.close(ax.figure)
print("-> example_output/12_correlation.png")
