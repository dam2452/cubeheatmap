<h1 align="center">cubeheatmap</h1>

<p align="center">
  <strong>Publication-quality square-cell heatmaps for matplotlib</strong>
</p>

<p align="center">
  <a href="https://pypi.org/project/cubeheatmap/"><img src="https://img.shields.io/pypi/v/cubeheatmap.svg" alt="PyPI"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-CC%20BY--NC%204.0-green.svg" alt="License"/></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+"/>
</p>

---

**cubeheatmap** renders clean, equal-sized square-cell heatmaps designed for scientific publications, reports, and presentations. Works with numpy arrays, pandas DataFrames, and any 2-D numerical data.

<p align="center">
  <img src="https://raw.githubusercontent.com/dam2452/cubeheatmap/main/example_output/12_correlation.svg" alt="cubeheatmap preview" width="500"/>
</p>

## Features

- **Square cells** - every cell is a perfect square, sized automatically
- **Multiple input formats** - `from_matrix()`, `from_dataframe()`
- **Annotations** - display values inside cells with auto-contrast text
- **Significance markers** - overlay stars or custom symbols with `sig_mask`
- **Grid layouts** - `draw_grid()` for multi-panel figures
- **Fully customisable** - 36+ style parameters: colors, fonts, rounded corners, dark themes
- **Domain presets** - citation networks, software dependencies, data pipelines, web graphs, social networks

## Installation

```bash
pip install cubeheatmap
```

## Quick Start

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

For presets, customization and transforms see **[docs/usage.md](docs/usage.md)**.

## Gallery

<table>
  <tr>
    <td align="center"><b>Annotated</b></td>
    <td align="center"><b>Significance markers</b></td>
    <td align="center"><b>Dark theme</b></td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/dam2452/cubeheatmap/main/example_output/4_annotated.svg" width="300"/></td>
    <td><img src="https://raw.githubusercontent.com/dam2452/cubeheatmap/main/example_output/5_sig_mask.svg" width="300"/></td>
    <td><img src="https://raw.githubusercontent.com/dam2452/cubeheatmap/main/example_output/8_dark_theme.svg" width="300"/></td>
  </tr>
  <tr>
    <td align="center"><b>Grid layout</b></td>
    <td align="center"><b>Rounded corners</b></td>
    <td align="center"><b>Likert survey</b></td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/dam2452/cubeheatmap/main/example_output/6_grid.svg" width="300"/></td>
    <td><img src="https://raw.githubusercontent.com/dam2452/cubeheatmap/main/example_output/7_rounded.svg" width="300"/></td>
    <td><img src="https://raw.githubusercontent.com/dam2452/cubeheatmap/main/example_output/13_survey.svg" width="300"/></td>
  </tr>
  <tr>
    <td align="center"><b>Citation network</b></td>
    <td align="center"><b>Model benchmark</b></td>
    <td align="center"><b>Dense microarray</b></td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/dam2452/cubeheatmap/main/example_output/9_citation_network.svg" width="300"/></td>
    <td><img src="https://raw.githubusercontent.com/dam2452/cubeheatmap/main/example_output/14_model_comparison.svg" width="300"/></td>
    <td><img src="https://raw.githubusercontent.com/dam2452/cubeheatmap/main/example_output/16_dense_microarray.svg" width="300"/></td>
  </tr>
</table>

## Examples

16 runnable scripts covering all features and presets - see **[docs/examples.md](docs/examples.md)** for the full list with previews.

```bash
cd examples && python generate_all.py
```

## Citation

If you use **cubeheatmap** in a publication, please cite it:

**APA:**

> dam2452. (2026). cubeheatmap: Publication-quality square-cell heatmaps for Python (Version 0.1.0). https://github.com/dam2452/cubeheatmap

**BibTeX:**

```bibtex
@software{cubeheatmap2026,
  title   = {cubeheatmap: Publication-quality square-cell heatmaps for Python},
  author  = {dam2452},
  year    = {2026},
  version = {0.1.0},
  url     = {https://github.com/dam2452/cubeheatmap}
}
```

## Contributing

Contributions are welcome! Here's how you can help:

1. **Bug reports** - Open an issue with a minimal reproducible example
2. **Feature requests** - Open an issue describing the use case
3. **Code contributions** - Fork, create a feature branch, and open a pull request
4. **New presets** - Add a new submodule under `cubeheatmap/presets/` with a `to_heatmap()` function and an example

### Development setup

```bash
git clone https://github.com/dam2452/cubeheatmap.git
cd cubeheatmap
pip install -e ".[dev]"
pytest tests/
```

## License

This project is licensed under **CC BY-NC 4.0** - [Creative Commons Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/).

- **Use it freely** - for research, education, personal projects
- **Cite the author** - attribution required in publications and derivative works
- **No commercial use** - you may not sell or monetize this software

See [LICENSE](LICENSE) for full details.
