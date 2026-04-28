"""Data pipeline / ETL stage comparison matrices as heatmaps."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np

from ..heatmap import CubeHeatmap
from ..style import Style


def stage_comparison_matrix(
    steps: List[Dict],
) -> CubeHeatmap:
    """Build a stage × stage connectivity matrix from pipeline step dicts.

    Parameters
    ----------
    steps:
        Each dict has ``name`` (str) and optionally ``inputs`` / ``outputs``
        (lists of data identifiers).  Cell ``[i, j] = 1`` when stage *i*
        produces an output that stage *j* consumes as input.
    """
    names = [s["name"] for s in steps]
    n = len(steps)
    idx = {name: i for i, name in enumerate(names)}
    matrix = np.zeros((n, n), dtype=float)

    for i, step in enumerate(steps):
        outputs = set(step.get("outputs", []))
        for j, other in enumerate(steps):
            inputs = set(other.get("inputs", []))
            if outputs & inputs:
                matrix[i, j] = 1.0
    return CubeHeatmap.from_matrix(matrix, row_labels=names, col_labels=names)


def throughput_matrix(
    steps: List[Dict],
    weight_key: str = "throughput",
) -> CubeHeatmap:
    """Build a stage × stage throughput matrix.

    Like :func:`stage_comparison_matrix` but cell values come from a numeric
    field (default ``"throughput"``) on the downstream step.

    Parameters
    ----------
    steps:
        Each dict has ``name``, ``inputs``, ``outputs``, and a numeric field
        keyed by *weight_key*.
    weight_key:
        Dict key holding the numeric weight value.
    """
    names = [s["name"] for s in steps]
    n = len(steps)
    matrix = np.zeros((n, n), dtype=float)

    for i, step in enumerate(steps):
        outputs = set(step.get("outputs", []))
        for j, other in enumerate(steps):
            inputs = set(other.get("inputs", []))
            if outputs & inputs:
                matrix[i, j] = float(other.get(weight_key, 1.0))
    return CubeHeatmap.from_matrix(matrix, row_labels=names, col_labels=names)


def from_dag(
    edges: List[Tuple[str, str, float]],
) -> CubeHeatmap:
    """Build a heatmap from a DAG edge list.

    Parameters
    ----------
    edges:
        List of ``(source, target, weight)`` tuples.
    """
    nodes = sorted({e[0] for e in edges} | {e[1] for e in edges})
    n = len(nodes)
    idx = {node: i for i, node in enumerate(nodes)}
    matrix = np.zeros((n, n), dtype=float)
    for src, tgt, w in edges:
        matrix[idx[src], idx[tgt]] = w
    return CubeHeatmap.from_matrix(matrix, row_labels=nodes, col_labels=nodes)


def to_heatmap(
    steps: List[Dict],
) -> Tuple[CubeHeatmap, Style]:
    """Convenience: return ``(CubeHeatmap, Style)`` for a pipeline plot."""
    hm = stage_comparison_matrix(steps)
    style = Style(
        cmap="YlOrRd",
        vmin=0,
        colorbar_label="Data flow",
        annotate=True,
        annotate_fmt="{:.0f}",
        col_label_rotation=45.0,
    )
    return hm, style
