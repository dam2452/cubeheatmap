# pylint: disable=duplicate-code
"""14 - ML model benchmark comparison."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import cubeheatmap as ch

OUT = "example_output"

models = ["Random Forest", "XGBoost", "Neural Net", "SVM", "KNN", "Logistic Reg."]
datasets = ["MNIST", "CIFAR-10", "Tabular-1", "Tabular-2", "NLP-SENT"]

rng = np.random.default_rng(99)
scores = rng.uniform(0.65, 0.98, (len(models), len(datasets)))

hm = ch.CubeHeatmap.from_matrix(scores, row_labels=models, col_labels=datasets)

style = ch.Style(
    cmap="YlGn",
    vmin=0.6,
    vmax=1.0,
    colorbar_label="Accuracy",
    cell_size=0.7,
    cell_gap=0.06,
    annotate=True,
    annotate_fmt="{:.2f}",
    annotate_fontsize=8.0,
    col_label_rotation=25.0,
)
ax = ch.draw(hm, title="ML Model Benchmark", subtitle="Accuracy across datasets", style=style)
ax.figure.savefig(f"{OUT}/14_model_comparison.svg", bbox_inches="tight")
plt.close(ax.figure)
print(f"  {OUT}/14_model_comparison.svg")
