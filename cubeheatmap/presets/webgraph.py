"""Web page link and similarity matrices as heatmaps."""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np

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
    pages = sorted(link_dict.keys())
    n = len(pages)
    idx = {p: i for i, p in enumerate(pages)}

    all_pages = set(pages)
    for targets in link_dict.values():
        all_pages.update(targets)
    all_pages = sorted(all_pages)

    if len(all_pages) > n:
        pages = all_pages
        n = len(pages)
        idx = {p: i for i, p in enumerate(pages)}

    matrix = np.zeros((n, n), dtype=float)
    for page, targets in link_dict.items():
        if page not in idx:
            continue
        for target in targets:
            if target in idx:
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
        style = Style(
            cmap="magma",
            vmin=0,
            vmax=1,
            colorbar_label="Jaccard similarity",
            annotate=True,
            annotate_fmt="{:.2f}",
            col_label_rotation=45.0,
        )
    else:
        hm = link_matrix(link_dict)
        style = Style(
            cmap="Blues",
            vmin=0,
            colorbar_label="Link count",
            annotate=True,
            annotate_fmt="{:.0f}",
            col_label_rotation=45.0,
        )
    return hm, style
