"""Bibliographic co-citation and collaboration matrices as heatmaps."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ..heatmap import CubeHeatmap
from ..style import Style


def parse_bibtex(path: str | Path) -> List[Dict[str, str]]:
    """Parse a ``.bib`` file and return a list of entry dicts.

    Each dict has at least: ``key``, ``type``, and whatever fields are
    present (``title``, ``author``, ``year``, ``journal``, …).
    """
    text = Path(path).read_text(encoding="utf-8")
    entries: List[Dict[str, str]] = []
    for match in re.finditer(
        r"@(\w+)\s*\{\s*([^,]+),\s*(.*?)\n\s*\}",
        text,
        re.DOTALL,
    ):
        entry: Dict[str, str] = {
            "type": match.group(1).lower(),
            "key": match.group(2).strip(),
        }
        for field_match in re.finditer(
            r"(\w+)\s*=\s*\{([^}]*)\}", match.group(3)
        ):
            entry[field_match.group(1).lower()] = field_match.group(2).strip()
        entries.append(entry)
    return entries


def co_citation_matrix(
    papers: List[str],
    citation_map: Dict[str, List[str]],
) -> CubeHeatmap:
    """Build a paper × paper co-citation count matrix.

    Parameters
    ----------
    papers:
        Ordered list of paper identifiers (become both row and column labels).
    citation_map:
        Mapping ``paper → [list of referenced papers]``.
        Shared references increment the co-citation count.
    """
    n = len(papers)
    ref_sets = {p: set(citation_map.get(p, [])) for p in papers}
    matrix = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i, n):
            shared = len(ref_sets[papers[i]] & ref_sets[papers[j]])
            matrix[i, j] = shared
            matrix[j, i] = shared
    return CubeHeatmap.from_matrix(matrix, row_labels=papers, col_labels=papers)


def author_collaboration_matrix(
    authors: List[str],
    author_papers: Dict[str, List[str]],
    paper_authors: Dict[str, List[str]],
) -> CubeHeatmap:
    """Build an author × author co-authorship count matrix.

    Parameters
    ----------
    authors:
        Ordered list of author names.
    author_papers:
        Mapping ``author → [list of paper IDs]``.
    paper_authors:
        Mapping ``paper → [list of author names]``.
    """
    n = len(authors)
    matrix = np.zeros((n, n), dtype=float)
    author_idx = {a: i for i, a in enumerate(authors)}
    for paper, pa_list in paper_authors.items():
        for i_idx in range(len(pa_list)):
            for j_idx in range(i_idx + 1, len(pa_list)):
                a_i = pa_list[i_idx]
                a_j = pa_list[j_idx]
                if a_i in author_idx and a_j in author_idx:
                    ii, jj = author_idx[a_i], author_idx[a_j]
                    matrix[ii, jj] += 1
                    matrix[jj, ii] += 1
    np.fill_diagonal(matrix, 0)
    return CubeHeatmap.from_matrix(matrix, row_labels=authors, col_labels=authors)


def to_heatmap(
    papers: List[str],
    citation_map: Dict[str, List[str]],
) -> Tuple[CubeHeatmap, Style]:
    """Convenience: return ``(CubeHeatmap, Style)`` for a co-citation plot."""
    hm = co_citation_matrix(papers, citation_map)
    style = Style(
        cmap="YlOrRd",
        vmin=0,
        colorbar_label="Shared references",
        cell_gap=0.06,
        annotate=True,
        annotate_fmt="{:.0f}",
        col_label_rotation=45.0,
    )
    return hm, style
