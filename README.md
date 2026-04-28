<p align="center">
  <img src="example_output/06_grid.png" alt="cubeheatmap grid preview" width="700">
</p>

<h1 align="center">cubeheatmap</h1>

<p align="center">
  <strong>Publication-quality square-cell heatmaps for matplotlib</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/cubeheatmap/"><img src="https://img.shields.io/pypi/v/cubeheatmap.svg" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python">
</p>

---

<!-- Replace the GIF below with an actual demo animation -->
<!-- ![demo](docs/images/demo.gif) -->

**cubeheatmap** renders clean, equal-sized square-cell heatmaps designed for scientific publications, reports, and presentations. Works with numpy arrays, pandas DataFrames, and any 2-D numerical data.

## Features

- **Square cells** — every cell is a perfect square, sized automatically
- **Multiple input formats** — `from_matrix()`, `from_dataframe()`
- **Annotations** — display values inside cells with auto-contrast text
- **Significance markers** — overlay stars or custom symbols with `sig_mask`
- **Grid layouts** — `draw_grid()` for multi-panel figures
- **Fully customisable** — 36+ style parameters: colors, fonts, rounded corners, dark themes
- **Domain presets** — citation networks, software dependencies, data pipelines, web graphs, social networks

## Installation

```bash
pip install cubeheatmap
```

From source:

```bash
git clone https://github.com/dam2452/cubeheatmap.git
cd cubeheatmap
pip install -e .
```

## Quick start

```python
import numpy as np
import cubeheatmap as ch

data = np.random.uniform(-4, 4, (10, 3))
hm = ch.CubeHeatmap.from_matrix(
    data,
    row_labels=[f"Gene_{i}" for i in range(10)],
    col_labels=["Day14", "Day21", "Day40"],
)

style = ch.Style(cmap="RdBu_r", vmin=-4, vmax=4, colorbar_label="log2FC")
ax = ch.draw(hm, title="My Heatmap", style=style)

ax.figure.savefig("heatmap.png", dpi=150, bbox_inches="tight")
```

## Gallery

<p align="center">
  <img src="example_output/01_from_matrix.png" width="220">
  <img src="example_output/04_annotated.png" width="220">
  <img src="example_output/08_dark_theme.png" width="220">
</p>
<p align="center">
  <img src="example_output/06_grid.png" width="220">
  <img src="example_output/07_rounded.png" width="220">
  <img src="example_output/12_correlation.png" width="220">
</p>
<p align="center">
  <img src="example_output/09_citation_network.png" width="220">
  <img src="example_output/10_dependencies.png" width="220">
  <img src="example_output/14_model_comparison.png" width="220">
</p>

## Examples

All 16 examples are self-contained scripts in `examples/`:

| # | File | Description |
|---|------|-------------|
| 01 | `from_matrix.py` | Basic matrix input |
| 02 | `from_dataframe.py` | Pandas DataFrame input |
| 03 | `top_n_rows.py` | Automatic top-N row selection |
| 04 | `annotated.py` | Cell value annotations |
| 05 | `sig_mask.py` | Significance markers |
| 06 | `grid.py` | Multi-panel grid layout |
| 07 | `rounded.py` | Rounded cell corners |
| 08 | `dark_theme.py` | Dark background theme |
| 09 | `citation_network.py` | Citation co-citation matrix |
| 10 | `dependencies.py` | Software dependency adjacency |
| 11 | `pipeline.py` | ETL pipeline connectivity |
| 12 | `correlation.py` | Feature correlation matrix |
| 13 | `survey.py` | Likert-scale survey results |
| 14 | `model_comparison.py` | ML model benchmarks |
| 15 | `webgraph.py` | Website link graph |
| 16 | `dense_microarray.py` | Dense microarray-style tiny cells |

Generate all outputs:

```bash
cd examples && python generate_all.py
```

## Domain Presets

### Citations

```python
from cubeheatmap.presets import citations

papers = ["Smith 2020", "Jones 2021", "Lee 2019", ...]
citation_map = {"Smith 2020": ["Lee 2019"], "Jones 2021": ["Smith 2020", "Lee 2019"], ...}

hm, style = citations.to_heatmap(papers, citation_map)
ch.draw(hm, title="Co-citation Network", style=style)
```

### Dependencies

```python
from cubeheatmap.presets import dependencies

deps = {"flask": ["werkzeug", "jinja2"], "jinja2": ["markupsafe"], ...}

hm, style = dependencies.to_heatmap(deps)
ch.draw(hm, title="Dependency Graph", style=style)
```

### Pipeline

```python
from cubeheatmap.presets import pipeline

steps = [
    {"name": "Extract", "inputs": [], "outputs": ["raw"]},
    {"name": "Transform", "inputs": ["raw"], "outputs": ["clean"]},
    {"name": "Load", "inputs": ["clean"], "outputs": ["db"]},
]

hm, style = pipeline.to_heatmap(steps)
ch.draw(hm, title="ETL Pipeline", style=style)
```

### Web Graph

```python
from cubeheatmap.presets import webgraph

links = {"Home": ["About", "Blog"], "Blog": ["Home", "Post1"], ...}

hm, style = webgraph.to_heatmap(links)
ch.draw(hm, title="Website Links", style=style)
```

### Social Network

```python
from cubeheatmap.presets import social

edges = [("Alice", "Bob", 5), ("Bob", "Charlie", 3), ...]

hm, style = social.to_heatmap(edges)
ch.draw(hm, title="Social Interactions", style=style)
```

## API reference

### `CubeHeatmap` — data model

```python
hm = ch.CubeHeatmap.from_matrix(matrix, row_labels, col_labels)
hm = ch.CubeHeatmap.from_dataframe(df)

hm.top_n_rows(n, key="max_abs")   # select top rows
hm.clip(vmin, vmax)                # clip values
hm.select_rows(indices)            # subset rows
hm.value_range()                   # (min, max)
```

### `draw()` — single heatmap

```python
ax = ch.draw(heatmap, ax=None, *, title="", subtitle="", style=Style(), sig_mask=None)
```

### `draw_grid()` — multi-panel grid

```python
fig = ch.draw_grid(
    heatmaps,
    titles=None, subtitles=None, suptitle="",
    ncols=1, style=Style(), sig_masks=None,
)
```

### `Style` — visual configuration

```python
style = ch.Style(
    # Cell
    cell_size=1.0,         cell_gap=0.06,
    cell_rounding=0.0,     # 0.0–0.5 for rounded corners
    # Colormap
    cmap="RdBu_r",         vmin=None,  vmax=None,
    # Labels
    row_label_fontsize=9.0,  col_label_fontsize=10.0,
    col_label_rotation=90.0, row_label_color="#222222",
    # Annotations
    annotate=False,          annotate_fmt="{:.1f}",
    # Significance
    sig_marker="*",          sig_marker_fontsize=8.0,
    # Colorbar
    show_colorbar=True,      colorbar_label="",
    # Background
    fig_facecolor="#FFFFFF",  ax_facecolor="#FFFFFF",
    # Title
    title_fontsize=13.0,     title_color="#111111",
)
```

## Citation

If you use **cubeheatmap** in a publication, please cite it:

**BibTeX:**

```bibtex
@software{cubeheatmap,
  title   = {cubeheatmap: Publication-quality square-cell heatmaps for Python},
  author  = {dam2452 and contributors},
  year    = {2025},
  url     = {https://github.com/dam2452/cubeheatmap}
}
```

**APA:**

> dam2452. (2025). *cubeheatmap: Publication-quality square-cell heatmaps for Python*. https://github.com/dam2452/cubeheatmap

See [CITATION.cff](CITATION.cff) for the full citation metadata.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the [MIT License](LICENSE).
