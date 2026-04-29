# pylint: disable=duplicate-code
"""04 - Cell value annotations."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import cubeheatmap as ch

OUT = "example_output"

rng = np.random.default_rng(42)
TIMEPOINTS = ["Day14", "Day21", "Day40"]

hm = ch.CubeHeatmap.from_matrix(
    rng.uniform(-2, 2, (6, 3)),
    row_labels=[f"Gene_{i}" for i in range(6)],
    col_labels=TIMEPOINTS,
)

style = ch.Style(
    cmap="RdBu_r",
    vmin=-2,
    vmax=2,
    annotate=True,
    annotate_fmt="{:.2f}",
    cell_size=0.8,
    colorbar_label="LFC",
)
ax = ch.draw(hm, title="Annotated cells", style=style)
ax.figure.savefig(f"{OUT}/4_annotated.svg", bbox_inches="tight")
plt.close(ax.figure)
print(f"  {OUT}/4_annotated.svg")
