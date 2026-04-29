# pylint: disable=duplicate-code
"""13 - Survey / Likert-scale results."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import cubeheatmap as ch

OUT = "example_output"

questions = [
    "Q1: Satisfaction",
    "Q2: Ease of use",
    "Q3: Recommend",
    "Q4: Value",
    "Q5: Support",
    "Q6: Docs",
    "Q7: Performance",
    "Q8: Reliability",
]
demographics = ["18-24", "25-34", "35-44", "45-54", "55+"]

rng = np.random.default_rng(123)
scores = rng.uniform(2.0, 5.0, (len(questions), len(demographics)))

hm = ch.CubeHeatmap.from_matrix(scores, row_labels=questions, col_labels=demographics)

style = ch.Style(
    cmap="RdYlGn",
    vmin=1,
    vmax=5,
    colorbar_label="Mean score (1-5)",
    cell_size=0.65,
    cell_gap=0.06,
    annotate=True,
    annotate_fmt="{:.1f}",
    annotate_fontsize=8.0,
    col_label_rotation=0.0,
)
ax = ch.draw(hm, title="User Survey Results", subtitle="Mean Likert scores by age group", style=style)
ax.figure.savefig(f"{OUT}/13_survey.svg", bbox_inches="tight")
plt.close(ax.figure)
print(f"  {OUT}/13_survey.svg")
