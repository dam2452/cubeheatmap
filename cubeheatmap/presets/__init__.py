"""cubeheatmap.presets - domain-specific helpers for building heatmaps.

Each submodule provides parsers and builders that produce
:class:`~cubeheatmap.CubeHeatmap` objects for a specific data domain.
"""

from __future__ import annotations

from typing import (
    List,
    Tuple,
)

import numpy as np

from ..heatmap import CubeHeatmap
from ..style import Style


def _build_square_matrix(
    triples: List[Tuple[str, str, float]],
    *,
    accumulate: bool = False,
) -> CubeHeatmap:
    """Build a square matrix from ``(source, target, weight)`` triples.

    Parameters
    ----------
    triples:
        List of (source, target, weight) tuples.
    accumulate:
        If True, weights for repeated (source, target) pairs are summed.
        If False, later values overwrite earlier ones.
    """
    nodes = sorted({s for s, _, _ in triples} | {t for _, t, _ in triples})
    n = len(nodes)
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = np.zeros((n, n), dtype=float)
    for src, tgt, w in triples:
        if accumulate:
            matrix[idx[src], idx[tgt]] += w
        else:
            matrix[idx[src], idx[tgt]] = w
    return CubeHeatmap.from_matrix(matrix, row_labels=nodes, col_labels=nodes)


def _network_style(**overrides) -> Style:
    """Create a Style with common preset defaults for network/graph heatmaps."""
    defaults = {
        "annotate": True,
        "annotate_fmt": "{:.0f}",
        "col_label_rotation": 45.0,
    }
    defaults.update(overrides)
    return Style(**defaults)


from . import (
    citations,
    dependencies,
    pipeline,
    social,
    webgraph,
)
