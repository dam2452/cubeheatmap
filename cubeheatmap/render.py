"""Render a CubeHeatmap as perfect square cells onto matplotlib axes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    List,
    Optional,
    Tuple,
)

import matplotlib.cm as mcm
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

from .heatmap import CubeHeatmap
from .style import (
    Style,
    default_style,
)

# ── Geometry helper ──────────────────────────────────────────────

@dataclass(frozen=True)
class _Geometry:
    """Pre-computed layout constants for square-cell grid placement."""

    sz: float
    gap: float
    step: float
    total_w: float
    total_h: float
    margin: float
    n_rows: int
    n_cols: int

    @classmethod
    def from_style(cls, heatmap: CubeHeatmap, style: Style) -> _Geometry:
        sz = style.cell_size
        gap = style.cell_gap
        step = sz + gap
        n_rows = heatmap.n_rows
        n_cols = heatmap.n_cols
        return cls(
            sz=sz,
            gap=gap,
            step=step,
            total_w=n_cols * step - gap,
            total_h=n_rows * step - gap,
            margin=gap,
            n_rows=n_rows,
            n_cols=n_cols,
        )

    def cell_xy(self, row: int, col: int) -> tuple[float, float]:
        """Return (x, y) for the lower-left corner of cell at (row, col)."""
        return col * self.step, (self.n_rows - 1 - row) * self.step

    def cell_center(self, row: int, col: int) -> tuple[float, float]:
        """Return (cx, cy) center of cell at (row, col)."""
        x, y = self.cell_xy(row, col)
        return x + self.sz / 2, y + self.sz / 2


# ── Public API ───────────────────────────────────────────────────

def draw(
    heatmap: CubeHeatmap,
    ax: Optional[plt.Axes] = None,
    *,
    title: str = "",
    subtitle: str = "",
    style: Style = default_style,
    sig_mask: Optional[np.ndarray] = None,
) -> plt.Axes:
    """Draw *heatmap* as square cells on *ax* (creates figure+ax if None).

    Parameters
    ----------
    heatmap:
        Data model produced by :class:`CubeHeatmap`.
    ax:
        Existing axes to draw on. A new figure is created when ``None``.
    title:
        Bold title rendered above the axes.
    subtitle:
        Lighter subtitle rendered below the title.
    style:
        :class:`Style` instance controlling all visual parameters.
    sig_mask:
        Boolean array of shape ``(n_rows, n_cols)``. Cells where ``True``
        receive a significance marker on top.
    """
    geo = _Geometry.from_style(heatmap, style)

    if ax is None:
        fig_w, fig_h = _figure_size(geo, style)
        _, ax = plt.subplots(figsize=(fig_w, fig_h))

    ax.figure.patch.set_facecolor(style.fig_facecolor)
    ax.set_facecolor(style.ax_facecolor)

    norm, cmap_obj = _build_norm_cmap(heatmap, style)
    _draw_cells(ax, heatmap, geo, norm, cmap_obj, style, sig_mask)
    _set_ticks(ax, heatmap, geo, style)
    _finalize_axes(ax, geo, style)

    if style.show_colorbar:
        _add_colorbar(ax, geo, norm, cmap_obj, style)

    _draw_title(ax, title, subtitle, style)
    return ax


def draw_grid(
    heatmaps: List[CubeHeatmap],
    *,
    titles: Optional[List[str]] = None,
    subtitles: Optional[List[str]] = None,
    suptitle: str = "",
    ncols: int = 1,
    style: Style = default_style,
    sig_masks: Optional[List[Optional[np.ndarray]]] = None,
) -> plt.Figure:
    """Draw multiple heatmaps in a grid layout and return the figure."""
    n = len(heatmaps)
    nrows = (n + ncols - 1) // ncols
    _titles = titles or [""] * n
    _subtitles = subtitles or [""] * n
    _masks = sig_masks or [None] * n

    step = style.cell_size + style.cell_gap
    label_w = style.grid_row_label_width
    title_h = style.grid_title_height
    col_label_h = style.grid_col_label_height

    row_data_heights = [hm.n_rows * step for hm in heatmaps]
    col_data_widths = [hm.n_cols * step for hm in heatmaps]

    grid_row_heights: List[float] = []
    for grid_row in range(nrows):
        col_idxs = range(grid_row * ncols, min(grid_row * ncols + ncols, n))
        grid_row_heights.append(max(row_data_heights[i] for i in col_idxs) + title_h + col_label_h)

    max_col_data_w = max(col_data_widths) if col_data_widths else step
    fig_w = (max_col_data_w + label_w) * ncols
    fig_h = sum(grid_row_heights) + style.grid_pad

    fig, axes = plt.subplots(
        nrows, ncols,
        figsize=(fig_w, fig_h),
        gridspec_kw={"height_ratios": grid_row_heights},
        squeeze=False,
    )
    fig.patch.set_facecolor(style.fig_facecolor)

    for idx, (hm, ax) in enumerate(zip(heatmaps, axes.flat)):
        draw(
            hm, ax, title=_titles[idx], subtitle=_subtitles[idx],
            style=style, sig_mask=_masks[idx],
        )

    for idx in range(n, nrows * ncols):
        axes.flat[idx].axis("off")

    if suptitle:
        kwargs = {
            "fontsize": style.grid_suptitle_fontsize if style.grid_suptitle_fontsize is not None else style.title_fontsize + 2,
            "fontweight": style.title_fontweight,
            "color": style.title_color,
        }
        if style.grid_suptitle_y is not None:
            kwargs["y"] = style.grid_suptitle_y
        fig.suptitle(suptitle, **kwargs)

    fig.tight_layout(pad=style.grid_pad)
    return fig


# ── Internal helpers ─────────────────────────────────────────────

def _build_norm_cmap(
    heatmap: CubeHeatmap,
    style: Style,
) -> Tuple[mcolors.Normalize, mcolors.Colormap]:
    vmin = style.vmin if style.vmin is not None else float(heatmap.matrix.min())
    vmax = style.vmax if style.vmax is not None else float(heatmap.matrix.max())
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    try:
        cmap_obj = plt.colormaps[style.cmap]
    except (KeyError, AttributeError):
        cmap_obj = mcm.get_cmap(style.cmap)
    return norm, cmap_obj


def _make_cell_patch(
    x: float,
    y: float,
    sz: float,
    color: tuple,
    style: Style,
) -> mpatches.Patch:
    if style.cell_rounding > 0:
        return mpatches.FancyBboxPatch(
            (x, y), sz, sz,
            boxstyle=f"round,pad=0,rounding_size={style.cell_rounding * sz}",
            facecolor=color,
            edgecolor=style.cell_edgecolor,
            linewidth=style.cell_edgewidth,
        )
    return mpatches.Rectangle(
        (x, y), sz, sz,
        facecolor=color,
        edgecolor=style.cell_edgecolor,
        linewidth=style.cell_edgewidth,
    )


def _draw_annotation(
    ax: plt.Axes,
    cx: float,
    cy: float,
    val: float,
    norm: mcolors.Normalize,
    style: Style,
) -> None:
    text_color = "white" if norm(val) < style.annotate_color_threshold else "black"
    ax.text(
        cx, cy, style.annotate_fmt.format(val),
        ha="center", va="center",
        fontsize=style.annotate_fontsize,
        color=text_color,
    )


def _draw_sig_marker(
    ax: plt.Axes,
    cx: float,
    cy: float,
    sz: float,
    style: Style,
) -> None:
    ax.text(
        cx, cy + sz * 0.28, style.sig_marker,
        ha="center", va="center",
        fontsize=style.sig_marker_fontsize,
        color=style.sig_marker_color,
    )


def _draw_cells(
    ax: plt.Axes,
    heatmap: CubeHeatmap,
    geo: _Geometry,
    norm: mcolors.Normalize,
    cmap_obj: mcolors.Colormap,
    style: Style,
    sig_mask: Optional[np.ndarray],
) -> None:
    for row_idx in range(geo.n_rows):
        for col_idx in range(geo.n_cols):
            val = heatmap.matrix[row_idx, col_idx]
            color = cmap_obj(norm(val))
            x, y = geo.cell_xy(row_idx, col_idx)

            ax.add_patch(_make_cell_patch(x, y, geo.sz, color, style))

            if style.annotate:
                cx, cy = geo.cell_center(row_idx, col_idx)
                _draw_annotation(ax, cx, cy, val, norm, style)

            if sig_mask is not None and sig_mask[row_idx, col_idx]:
                cx, cy = geo.cell_center(row_idx, col_idx)
                _draw_sig_marker(ax, cx, cy, geo.sz, style)


def _set_ticks(
    ax: plt.Axes,
    heatmap: CubeHeatmap,
    geo: _Geometry,
    style: Style,
) -> None:
    col_positions = [i * geo.step + geo.sz / 2 for i in range(geo.n_cols)]
    row_positions = [(geo.n_rows - 1 - i) * geo.step + geo.sz / 2 for i in range(geo.n_rows)]

    ax.set_xticks(col_positions)
    ax.set_xticklabels(
        heatmap.col_labels,
        fontsize=style.col_label_fontsize,
        fontweight=style.col_label_fontweight,
        rotation=style.col_label_rotation,
        ha=style.col_label_ha,
        va="top",
        color=style.col_label_color,
    )
    ax.xaxis.set_tick_params(pad=style.col_label_pad)

    ax.set_yticks(row_positions)
    ax.set_yticklabels(
        heatmap.row_labels,
        fontsize=style.row_label_fontsize,
        color=style.row_label_color,
    )
    ax.yaxis.set_tick_params(pad=style.row_label_pad)

    ax.tick_params(axis="both", length=0)


def _finalize_axes(
    ax: plt.Axes,
    geo: _Geometry,
    style: Style,
) -> None:
    ax.set_xlim(-geo.margin, geo.total_w + geo.margin)
    ax.set_ylim(-geo.margin, geo.total_h + geo.margin)
    ax.set_aspect("equal")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.set_facecolor(style.ax_facecolor)


def _add_colorbar(
    ax: plt.Axes,
    geo: _Geometry,
    norm: mcolors.Normalize,
    cmap_obj: mcolors.Colormap,
    style: Style,
) -> None:
    cbar_x = geo.total_w + geo.margin + style.colorbar_pad * geo.sz
    cbar_w = geo.total_w * style.colorbar_width_frac
    cax = ax.inset_axes(
        [cbar_x, 0, cbar_w, geo.total_h],
        transform=ax.transData,
    )

    sm = plt.cm.ScalarMappable(cmap=cmap_obj, norm=norm)
    sm.set_array([])
    cbar = ax.figure.colorbar(sm, cax=cax)
    if style.colorbar_label:
        cbar.set_label(
            style.colorbar_label,
            fontsize=style.colorbar_fontsize,
            color=style.row_label_color,
        )
    cbar.ax.tick_params(
        labelsize=style.colorbar_tick_fontsize,
        colors=style.row_label_color,
    )
    for spine in cbar.ax.spines.values():
        spine.set_edgecolor(style.spine_color)


def _draw_title(
    ax: plt.Axes,
    title: str,
    subtitle: str,
    style: Style,
) -> None:
    if not title and not subtitle:
        return
    full = f"{title}\n{subtitle}" if title and subtitle else (title or subtitle)
    ax.set_title(
        full,
        fontsize=style.title_fontsize,
        fontweight=style.title_fontweight,
        color=style.title_color,
        pad=style.title_pad,
    )


def _figure_size(geo: _Geometry, style: Style) -> Tuple[float, float]:
    base_w = geo.n_cols * geo.step + style.grid_row_label_width
    base_h = geo.n_rows * geo.step + style.grid_title_height + style.grid_col_label_height
    return base_w, base_h
