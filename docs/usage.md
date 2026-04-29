# Usage

## Input Formats

| Method | Description | Use case |
|--------|-------------|----------|
| `from_matrix()` | From a list-of-lists or numpy array | Numerical data, custom matrices |
| `from_dataframe()` | From a pandas DataFrame | Data already in DataFrames |

```python
import cubeheatmap as ch

hm = ch.CubeHeatmap.from_matrix(matrix, row_labels, col_labels)
hm = ch.CubeHeatmap.from_dataframe(df)
```

## Domain Presets

### Citations

```python
from cubeheatmap.presets import citations

papers = ["Smith 2020", "Jones 2021", "Lee 2019"]
citation_map = {"Smith 2020": ["Lee 2019"], "Jones 2021": ["Smith 2020", "Lee 2019"]}

hm, style = citations.to_heatmap(papers, citation_map)
ch.draw(hm, title="Co-citation Network", style=style)
```

### Dependencies

```python
from cubeheatmap.presets import dependencies

deps = {"flask": ["werkzeug", "jinja2"], "jinja2": ["markupsafe"]}

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

links = {"Home": ["About", "Blog"], "Blog": ["Home", "Post1"]}

hm, style = webgraph.to_heatmap(links)
ch.draw(hm, title="Website Links", style=style)
```

### Social Network

```python
from cubeheatmap.presets import social

edges = [("Alice", "Bob", 5), ("Bob", "Charlie", 3)]

hm, style = social.to_heatmap(edges)
ch.draw(hm, title="Social Interactions", style=style)
```

## Customization

### Style

```python
from cubeheatmap import Style

my_style = Style(
    # Cell
    cell_size=1.0,
    cell_gap=0.06,
    cell_rounding=0.15,
    cell_edgecolor="none",
    # Colormap
    cmap="RdBu_r",
    vmin=-4,
    vmax=4,
    # Labels
    row_label_fontsize=9.0,
    col_label_fontsize=10.0,
    col_label_rotation=45.0,
    # Annotations
    annotate=True,
    annotate_fmt="{:.2f}",
    annotate_fontsize=7.0,
    # Significance
    sig_marker="*",
    sig_marker_fontsize=8.0,
    # Colorbar
    show_colorbar=True,
    colorbar_label="log2FC",
    # Background
    fig_facecolor="#FFFFFF",
    ax_facecolor="#FFFFFF",
    # Title
    title_fontsize=13.0,
    title_color="#111111",
)

ax = ch.draw(heatmap, style=my_style, title="Custom Styled")
```

### Data Transforms

```python
hm_top = hm.top_n_rows(20, key="max_abs")
hm_clipped = hm.clip(-3, 3)
hm_subset = hm.select_rows([0, 2, 5])
vmin, vmax = hm.value_range()
```

### Multi-Panel Grids

```python
fig = ch.draw_grid(
    [hm1, hm2, hm3, hm4],
    titles=["Panel A", "Panel B", "Panel C", "Panel D"],
    suptitle="Comparison",
    ncols=2,
    style=style,
)
```
