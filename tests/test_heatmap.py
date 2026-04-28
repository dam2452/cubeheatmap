"""Tests for CubeHeatmap data model."""

import numpy as np
import pandas as pd
import pytest

from cubeheatmap.heatmap import CubeHeatmap


# ── Constructors ──────────────────────────────────────────────────

class TestFromMatrix:

    def test_basic(self):
        hm = CubeHeatmap.from_matrix(
            [[1, 2], [3, 4]],
            row_labels=["A", "B"],
            col_labels=["X", "Y"],
        )
        assert hm.n_rows == 2
        assert hm.n_cols == 2
        assert hm.row_labels == ["A", "B"]
        assert hm.col_labels == ["X", "Y"]
        assert hm.matrix.dtype == float

    def test_1d_raises(self):
        with pytest.raises(ValueError, match="2-D"):
            CubeHeatmap.from_matrix([1, 2, 3], row_labels=["A"], col_labels=["X"])

    def test_wrong_row_labels_raises(self):
        with pytest.raises(ValueError, match="row_labels"):
            CubeHeatmap.from_matrix([[1, 2]], row_labels=["A", "B"], col_labels=["X"])

    def test_wrong_col_labels_raises(self):
        with pytest.raises(ValueError, match="col_labels"):
            CubeHeatmap.from_matrix([[1, 2]], row_labels=["A"], col_labels=["X", "Y", "Z"])


class TestFromDataframe:

    def test_basic(self):
        df = pd.DataFrame(
            [[1, 2], [3, 4]],
            index=["A", "B"],
            columns=["X", "Y"],
        )
        hm = CubeHeatmap.from_dataframe(df)
        assert hm.row_labels == ["A", "B"]
        assert hm.col_labels == ["X", "Y"]
        assert hm.n_rows == 2

    def test_with_metadata(self):
        df = pd.DataFrame([[5]], index=["R"], columns=["C"])
        hm = CubeHeatmap.from_dataframe(df, metadata={"source": "test"})
        assert hm.metadata["source"] == "test"


# ── Properties ────────────────────────────────────────────────────

class TestProperties:

    def test_n_rows_cols(self):
        hm = CubeHeatmap.from_matrix(
            np.zeros((3, 5)),
            row_labels=["A", "B", "C"],
            col_labels=[str(i) for i in range(5)],
        )
        assert hm.n_rows == 3
        assert hm.n_cols == 5

    def test_value_range(self):
        hm = CubeHeatmap.from_matrix(
            [[-3, 7], [0, 2]],
            row_labels=["A", "B"],
            col_labels=["X", "Y"],
        )
        assert hm.value_range() == (-3.0, 7.0)


# ── Transforms ────────────────────────────────────────────────────

class TestTransforms:

    def _make(self):
        return CubeHeatmap.from_matrix(
            [[-4, 6], [1, -2]],
            row_labels=["A", "B"],
            col_labels=["X", "Y"],
        )

    def test_clip(self):
        hm = self._make().clip(-2, 2)
        assert hm.matrix.min() == -2.0
        assert hm.matrix.max() == 2.0
        assert hm.row_labels == ["A", "B"]

    def test_select_rows(self):
        hm = self._make().select_rows([1])
        assert hm.n_rows == 1
        assert hm.row_labels == ["B"]
        assert hm.n_cols == 2

    def test_top_n_rows_max_abs(self):
        big = CubeHeatmap.from_matrix(
            [[10, 0], [1, 1], [5, 5]],
            row_labels=["A", "B", "C"],
            col_labels=["X", "Y"],
        )
        top = big.top_n_rows(2, key="max_abs")
        assert set(top.row_labels) == {"A", "C"}

    def test_top_n_rows_sum_abs(self):
        big = CubeHeatmap.from_matrix(
            [[1, 1], [5, -5], [2, 0]],
            row_labels=["A", "B", "C"],
            col_labels=["X", "Y"],
        )
        top = big.top_n_rows(1, key="sum_abs")
        assert top.row_labels == ["B"]

    def test_top_n_unknown_key_raises(self):
        hm = self._make()
        with pytest.raises(ValueError, match="Unknown key"):
            hm.top_n_rows(1, key="invalid")

    def test_transform_preserves_metadata(self):
        hm = CubeHeatmap.from_matrix(
            [[1, 2]], row_labels=["A"], col_labels=["X", "Y"],
            metadata={"note": "original"},
        )
        clipped = hm.clip(-1, 1)
        assert clipped.metadata["note"] == "original"
        # Ensure it's a copy
        clipped.metadata["note"] = "modified"
        assert hm.metadata["note"] == "original"
