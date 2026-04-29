"""Tests for draw() and draw_grid() rendering."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

from cubeheatmap.heatmap import CubeHeatmap
from cubeheatmap.render import (
    draw,
    draw_grid,
)
from cubeheatmap.style import Style


def _make_heatmap(n_rows=4, n_cols=3):
    rng = np.random.default_rng(0)
    return CubeHeatmap.from_matrix(
        rng.uniform(-1, 1, (n_rows, n_cols)),
        row_labels=[f"R{i}" for i in range(n_rows)],
        col_labels=[f"C{i}" for i in range(n_cols)],
    )


class TestDraw:

    def test_returns_axes(self):
        hm = _make_heatmap()
        ax = draw(hm)
        assert isinstance(ax, plt.Axes)
        plt.close(ax.figure)

    def test_creates_figure(self):
        hm = _make_heatmap()
        ax = draw(hm)
        assert ax.figure is not None
        plt.close(ax.figure)

    def test_on_existing_axes(self):
        fig, axes = plt.subplots(1, 2)
        hm = _make_heatmap()
        ax = draw(hm, ax=axes[0])
        assert ax is axes[0]
        plt.close(fig)

    def test_with_title(self):
        hm = _make_heatmap()
        ax = draw(hm, title="Test Title", subtitle="Test Sub")
        assert ax.get_title() != ""
        plt.close(ax.figure)

    def test_with_sig_mask(self):
        hm = _make_heatmap()
        mask = np.ones((hm.n_rows, hm.n_cols), dtype=bool)
        ax = draw(hm, sig_mask=mask)
        assert isinstance(ax, plt.Axes)
        plt.close(ax.figure)

    def test_custom_style(self):
        hm = _make_heatmap()
        style = Style(cmap="viridis", cell_rounding=0.1, annotate=True)
        ax = draw(hm, style=style)
        assert isinstance(ax, plt.Axes)
        plt.close(ax.figure)


class TestDrawGrid:

    def test_returns_figure(self):
        heatmaps = [_make_heatmap() for _ in range(4)]
        fig = draw_grid(heatmaps, ncols=2)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_grid_shape(self):
        heatmaps = [_make_heatmap() for _ in range(4)]
        fig = draw_grid(heatmaps, ncols=2)
        # 2x2 grid from 4 heatmaps
        assert len(fig.axes) == 4
        plt.close(fig)

    def test_with_suptitle(self):
        heatmaps = [_make_heatmap() for _ in range(2)]
        fig = draw_grid(heatmaps, suptitle="Grid Title", ncols=1)
        assert fig._suptitle is not None
        assert fig._suptitle.get_text() == "Grid Title"
        plt.close(fig)

    def test_with_titles(self):
        heatmaps = [_make_heatmap() for _ in range(2)]
        fig = draw_grid(
            heatmaps,
            titles=["Panel A", "Panel B"],
            ncols=1,
        )
        plt.close(fig)

    def test_extra_axes_hidden(self):
        heatmaps = [_make_heatmap() for _ in range(3)]
        fig = draw_grid(heatmaps, ncols=2)
        # 3 heatmaps in 2x2 grid → 4th axis is hidden
        assert len(fig.axes) == 4
        plt.close(fig)
