"""Social network interaction matrices as heatmaps."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from ..heatmap import CubeHeatmap
from ..style import Style


def interaction_matrix(
    edges: List[Tuple[str, str, float]],
) -> CubeHeatmap:
    """Build a user × user weighted interaction matrix from an edge list.

    Parameters
    ----------
    edges:
        List of ``(source, target, weight)`` tuples, e.g. interactions or
        follower counts.
    """
    users = sorted({e[0] for e in edges} | {e[1] for e in edges})
    n = len(users)
    idx = {u: i for i, u in enumerate(users)}
    matrix = np.zeros((n, n), dtype=float)
    for src, tgt, w in edges:
        matrix[idx[src], idx[tgt]] += w
    return CubeHeatmap.from_matrix(matrix, row_labels=users, col_labels=users)


def from_adjacency_file(
    path: str | Path,
    delimiter: str = ",",
    has_header: bool = True,
) -> CubeHeatmap:
    """Load an adjacency matrix from a CSV / TSV file.

    Parameters
    ----------
    path:
        Path to the file.
    delimiter:
        Column delimiter.
    has_header:
        If ``True``, the first row and column are treated as labels.
    """
    path = Path(path)
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    if has_header:
        col_labels = lines[0].split(delimiter)[1:]
        rows = [line.split(delimiter) for line in lines[1:]]
        row_labels = [r[0] for r in rows]
        data = [[float(v) for v in r[1:]] for r in rows]
    else:
        data = [[float(v) for v in line.split(delimiter)] for line in lines]
        n = len(data)
        row_labels = [f"R{i}" for i in range(n)]
        col_labels = [f"C{i}" for i in range(n)]
    return CubeHeatmap.from_matrix(
        np.array(data, dtype=float),
        row_labels=row_labels,
        col_labels=col_labels,
    )


def from_interaction_counts(
    counts: Dict[Tuple[str, str], float],
) -> CubeHeatmap:
    """Build a matrix from a dict of ``(source, target) → count`` pairs.

    Parameters
    ----------
    counts:
        Mapping of interaction pairs to their aggregated counts.
    """
    users = sorted({k[0] for k in counts} | {k[1] for k in counts})
    n = len(users)
    idx = {u: i for i, u in enumerate(users)}
    matrix = np.zeros((n, n), dtype=float)
    for (src, tgt), w in counts.items():
        matrix[idx[src], idx[tgt]] = w
    return CubeHeatmap.from_matrix(matrix, row_labels=users, col_labels=users)


def to_heatmap(
    edges: List[Tuple[str, str, float]],
) -> Tuple[CubeHeatmap, Style]:
    """Convenience: return ``(CubeHeatmap, Style)`` for a social network plot."""
    hm = interaction_matrix(edges)
    style = Style(
        cmap="Oranges",
        colorbar_label="Interactions",
        annotate=True,
        annotate_fmt="{:.0f}",
        col_label_rotation=45.0,
    )
    return hm, style
