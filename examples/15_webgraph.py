"""15 — Web graph preset (page link matrix)."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import cubeheatmap as ch

link_dict = {
    "Home":       ["About", "Blog", "Products", "Contact"],
    "About":      ["Home", "Team"],
    "Blog":       ["Home", "Post1", "Post2"],
    "Products":   ["Home", "Pricing", "Docs"],
    "Contact":    ["Home"],
    "Team":       ["About", "Home"],
    "Post1":      ["Blog", "Home", "Products"],
    "Post2":      ["Blog", "Home"],
    "Pricing":    ["Products", "Home", "Contact"],
    "Docs":       ["Products", "Home"],
}

hm, style = ch.presets.webgraph.to_heatmap(link_dict, mode="adjacency")
style.cell_size = 0.55
style.row_label_fontsize = 8.0
style.col_label_fontsize = 8.0

ax = ch.draw(hm, title="Website Link Graph", subtitle="Internal link adjacency matrix", style=style)
ax.figure.savefig("example_output/15_webgraph.png", dpi=150, bbox_inches="tight")
plt.close(ax.figure)
print("-> example_output/15_webgraph.png")
