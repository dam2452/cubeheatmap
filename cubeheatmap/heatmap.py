"""Core data model: CubeHeatmap."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


@dataclass
class CubeHeatmap:
    """2-D matrix rendered as equal square cells."""

    matrix: np.ndarray
    row_labels: List[str]
    col_labels: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.matrix.ndim != 2:
            raise ValueError(f"matrix must be 2-D, got shape {self.matrix.shape}")
        n_rows, n_cols = self.matrix.shape
        if len(self.row_labels) != n_rows:
            raise ValueError(
                f"row_labels length ({len(self.row_labels)}) != matrix rows ({n_rows})"
            )
        if len(self.col_labels) != n_cols:
            raise ValueError(
                f"col_labels length ({len(self.col_labels)}) != matrix cols ({n_cols})"
            )

    @property
    def n_rows(self) -> int:
        return self.matrix.shape[0]

    @property
    def n_cols(self) -> int:
        return self.matrix.shape[1]

    # ── Constructors ─────────────────────────────────────────────

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, **kwargs: Any) -> "CubeHeatmap":
        return cls(
            matrix=df.to_numpy(dtype=float),
            row_labels=list(df.index.astype(str)),
            col_labels=list(df.columns.astype(str)),
            **kwargs,
        )

    @classmethod
    def from_matrix(
        cls,
        matrix: List[List[float]],
        row_labels: List[str],
        col_labels: List[str],
        **kwargs: Any,
    ) -> "CubeHeatmap":
        return cls(
            matrix=np.array(matrix, dtype=float),
            row_labels=row_labels,
            col_labels=col_labels,
            **kwargs,
        )

    # ── Transforms ───────────────────────────────────────────────

    def clip(self, vmin: float, vmax: float) -> "CubeHeatmap":
        return CubeHeatmap(
            matrix=np.clip(self.matrix, vmin, vmax),
            row_labels=self.row_labels[:],
            col_labels=self.col_labels[:],
            metadata=dict(self.metadata),
        )

    def select_rows(self, indices: List[int]) -> "CubeHeatmap":
        return CubeHeatmap(
            matrix=self.matrix[indices],
            row_labels=[self.row_labels[i] for i in indices],
            col_labels=self.col_labels[:],
            metadata=dict(self.metadata),
        )

    def top_n_rows(self, n: int, key: str = "max_abs") -> "CubeHeatmap":
        if key == "max_abs":
            scores = np.abs(self.matrix).max(axis=1)
        elif key == "sum_abs":
            scores = np.abs(self.matrix).sum(axis=1)
        else:
            raise ValueError(f"Unknown key '{key}'. Use 'max_abs' or 'sum_abs'.")
        idx = list(np.argsort(-scores)[:n])
        return self.select_rows(idx)

    def value_range(self) -> Tuple[float, float]:
        return float(self.matrix.min()), float(self.matrix.max())
