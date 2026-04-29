# pylint: disable=duplicate-code
"""10 - Software dependency preset (adjacency matrix)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import cubeheatmap as ch

OUT = "example_output"

deps = {
    "flask":       ["werkzeug", "jinja2", "itsdangerous"],
    "werkzeug":    [],
    "jinja2":      ["markupsafe"],
    "itsdangerous":[],
    "markupsafe":  [],
    "click":       [],
    "sqlalchemy":  [],
    "alembic":     ["sqlalchemy", "markupsafe"],
}

hm, style = ch.presets.dependencies.to_heatmap(deps, mode="adjacency")
style.cell_size = 0.7

ax = ch.draw(hm, title="Software Dependencies", subtitle="Flask dependency tree adjacency", style=style)
ax.figure.savefig(f"{OUT}/10_dependencies.svg", bbox_inches="tight")
plt.close(ax.figure)
print(f"  {OUT}/10_dependencies.svg")
