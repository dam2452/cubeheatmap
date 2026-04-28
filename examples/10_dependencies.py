"""10 — Software dependency preset (adjacency matrix)."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import cubeheatmap as ch

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
ax.figure.savefig("example_output/10_dependencies.png", dpi=150, bbox_inches="tight")
plt.close(ax.figure)
print("-> example_output/10_dependencies.png")
