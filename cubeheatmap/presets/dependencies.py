"""Software dependency adjacency and depth matrices as heatmaps."""

from __future__ import annotations

import json
import re
from collections import deque
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from ..heatmap import CubeHeatmap
from ..style import Style


def parse_requirements(path: str | Path) -> Dict[str, List[str]]:
    """Parse a ``requirements.txt`` into ``{package: [dependencies]}``.

    Only extracts the top-level package name (no version pins, no extras).
    This returns a flat dict without actual transitive deps — use
    :func:`adjacency_matrix` with manual dependency data for full graphs.
    """
    text = Path(path).read_text(encoding="utf-8")
    packages: Dict[str, List[str]] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        name = re.split(r"[><=!~\[]", line)[0].strip().lower()
        packages[name] = []
    return packages


def parse_package_json(path: str | Path) -> Dict[str, List[str]]:
    """Parse ``package.json`` dependencies into ``{package: [deps]}``."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    deps: Dict[str, List[str]] = {}
    for section in ("dependencies", "devDependencies"):
        for name in data.get(section, {}):
            deps[name] = []
    return deps


def adjacency_matrix(deps: Dict[str, List[str]]) -> CubeHeatmap:
    """Build a package × package binary adjacency matrix.

    Parameters
    ----------
    deps:
        Mapping ``package → [list of direct dependencies]``.
        Cell ``[i, j] = 1`` if package *i* depends on package *j*.
    """
    packages = sorted(deps.keys())
    n = len(packages)
    idx = {p: i for i, p in enumerate(packages)}
    matrix = np.zeros((n, n), dtype=float)
    for pkg, dep_list in deps.items():
        if pkg not in idx:
            continue
        for dep in dep_list:
            if dep in idx:
                matrix[idx[pkg], idx[dep]] = 1.0
    return CubeHeatmap.from_matrix(matrix, row_labels=packages, col_labels=packages)


def depth_matrix(
    deps: Dict[str, List[str]],
    root: Optional[str] = None,
) -> CubeHeatmap:
    """Build a package × package depth-distance matrix via BFS.

    Parameters
    ----------
    deps:
        Mapping ``package → [list of direct dependencies]``.
    root:
        Starting package. If ``None``, uses the first key in *deps*.
    """
    packages = sorted(deps.keys())
    n = len(packages)
    idx = {p: i for i, p in enumerate(packages)}
    matrix = np.full((n, n), np.nan, dtype=float)

    for start_pkg in packages:
        si = idx[start_pkg]
        visited = {start_pkg: 0}
        queue = deque([start_pkg])
        while queue:
            node = queue.popleft()
            d = visited[node]
            ni = idx[node]
            matrix[si, ni] = d
            for dep in deps.get(node, []):
                if dep in idx and dep not in visited:
                    visited[dep] = d + 1
                    queue.append(dep)
    matrix = np.nan_to_num(matrix, nan=-1)
    return CubeHeatmap.from_matrix(matrix, row_labels=packages, col_labels=packages)


def to_heatmap(
    deps: Dict[str, List[str]],
    mode: str = "adjacency",
) -> Tuple[CubeHeatmap, Style]:
    """Convenience: return ``(CubeHeatmap, Style)`` for a dependency plot."""
    if mode == "adjacency":
        hm = adjacency_matrix(deps)
        style = Style(
            cmap="Blues",
            vmin=0,
            vmax=1,
            colorbar_label="Depends on",
            annotate=True,
            annotate_fmt="{:.0f}",
            col_label_rotation=45.0,
        )
    else:
        hm = depth_matrix(deps)
        style = Style(
            cmap="YlGnBu",
            colorbar_label="Dependency depth",
            annotate=True,
            annotate_fmt="{:.0f}",
            col_label_rotation=45.0,
        )
    return hm, style
