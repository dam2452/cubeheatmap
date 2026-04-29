# pylint: disable=duplicate-code
"""11 - Data pipeline preset (stage connectivity matrix)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import cubeheatmap as ch

OUT = "example_output"

steps = [
    {"name": "Extract API",    "inputs": [],                       "outputs": ["raw_json"]},
    {"name": "Parse JSON",     "inputs": ["raw_json"],             "outputs": ["parsed_df"]},
    {"name": "Validate",       "inputs": ["parsed_df"],            "outputs": ["clean_df"]},
    {"name": "Transform",      "inputs": ["clean_df"],             "outputs": ["features"]},
    {"name": "Load DB",        "inputs": ["features"],             "outputs": ["db_table"]},
    {"name": "Generate Report","inputs": ["db_table", "clean_df"], "outputs": ["report"]},
]

hm, style = ch.presets.pipeline.to_heatmap(steps)
style.cell_size = 0.7

ax = ch.draw(hm, title="ETL Pipeline", subtitle="Stage connectivity matrix", style=style)
ax.figure.savefig(f"{OUT}/11_pipeline.svg", bbox_inches="tight")
plt.close(ax.figure)
print(f"  {OUT}/11_pipeline.svg")
