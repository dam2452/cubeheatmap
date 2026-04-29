# pylint: disable=duplicate-code
"""02 - from_dataframe() with pandas input."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import cubeheatmap as ch

OUT = "example_output"

rng = np.random.default_rng(42)

df = pd.DataFrame(
    rng.uniform(-3, 3, (8, 4)),
    index=[f"Gene_{i}" for i in range(8)],
    columns=["Ctrl vs T1", "Ctrl vs T2", "Ctrl vs T3", "Ctrl vs T4"],
)
hm = ch.CubeHeatmap.from_dataframe(df)

style = ch.Style(
    cmap="coolwarm",
    vmin=-3,
    vmax=3,
    colorbar_label="LFC",
    col_label_rotation=30.0,
)
ax = ch.draw(hm, title="from_dataframe()", style=style)
ax.figure.savefig(f"{OUT}/2_from_dataframe.svg", bbox_inches="tight")
plt.close(ax.figure)
print(f"  {OUT}/2_from_dataframe.svg")
