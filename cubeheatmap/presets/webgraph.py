"""Web page link and similarity matrices as heatmaps."""

from __future__ import annotations

from typing import (
    Dict,
    List,
    Tuple,
)

import numpy as np

from . import _network_style
from ..heatmap import CubeHeatmap
from ..style import Style


def link_matrix(
    link_dict: Dict[str, List[str]],
) -> CubeHeatmap:
    """Build a page × page link-count adjacency matrix.

    Parameters
    ----------
    link_dict:
        Mapping ``page → [list of pages it links to]``.
        Cell ``[i, j]`` counts how many times page *i* links to page *j*.
    """
    pages = sorted(
        set(link_dict.keys())
        | {t for targets in link_dict.values() for t in targets},
    )
    n = len(pages)
    idx = {p: i for i, p in enumerate(pages)}

    matrix = np.zeros((n, n), dtype=float)
    for page, targets in link_dict.items():
        for target in targets:
            matrix[idx[page], idx[target]] += 1.0
    return CubeHeatmap.from_matrix(matrix, row_labels=pages, col_labels=pages)


def similarity_matrix(
    link_dict: Dict[str, List[str]],
) -> CubeHeatmap:
    """Build a page × page Jaccard similarity matrix based on outgoing links.

    For pages *i* and *j*: ``|out(i) ∩ out(j)| / |out(i) ∪ out(j)|``.
    """
    pages = sorted(link_dict.keys())
    n = len(pages)
    out_sets = {p: set(link_dict.get(p, [])) for p in pages}
    matrix = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i, n):
            si, sj = out_sets[pages[i]], out_sets[pages[j]]
            union = si | sj
            if union:
                sim = len(si & sj) / len(union)
            else:
                sim = 0.0
            matrix[i, j] = sim
            matrix[j, i] = sim
    return CubeHeatmap.from_matrix(matrix, row_labels=pages, col_labels=pages)


def to_heatmap(
    link_dict: Dict[str, List[str]],
    mode: str = "adjacency",
) -> Tuple[CubeHeatmap, Style]:
    """Convenience: return ``(CubeHeatmap, Style)`` for a web graph plot."""
    if mode == "similarity":
        hm = similarity_matrix(link_dict)
        style = _network_style(
            cmap="magma",
            vmin=0,
            vmax=1,
            colorbar_label="Jaccard similarity",
            annotate_fmt="{:.2f}",
        )
    else:
        hm = link_matrix(link_dict)
        style = _network_style(
            cmap="Blues",
            vmin=0,
            colorbar_label="Link count",
        )
    return hm, style
