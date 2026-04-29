# pylint: disable=duplicate-code
"""09 - Citation network preset (co-citation matrix)."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import cubeheatmap as ch

OUT = "example_output"

papers = [
    "Smith 2020",
    "Jones 2021",
    "Lee 2019",
    "Patel 2022",
    "Mueller 2020",
    "Chen 2021",
    "Garcia 2022",
    "Kim 2019",
]

citation_map = {
    "Smith 2020":  ["Lee 2019", "Kim 2019"],
    "Jones 2021":  ["Smith 2020", "Lee 2019", "Kim 2019"],
    "Lee 2019":    ["Kim 2019"],
    "Patel 2022":  ["Smith 2020", "Jones 2021", "Mueller 2020"],
    "Mueller 2020":["Lee 2019", "Chen 2021"],
    "Chen 2021":   ["Smith 2020", "Kim 2019"],
    "Garcia 2022": ["Jones 2021", "Patel 2022", "Chen 2021"],
    "Kim 2019":    [],
}

hm, style = ch.presets.citations.to_heatmap(papers, citation_map)
style.cell_size = 0.65

ax = ch.draw(hm, title="Co-citation Network", subtitle="Shared references between papers", style=style)
ax.figure.savefig(f"{OUT}/9_citation_network.svg", bbox_inches="tight")
plt.close(ax.figure)
print(f"  {OUT}/9_citation_network.svg")
