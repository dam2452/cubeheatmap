"""Style configuration for square-cell heatmap rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Style:
    # ── Cell ─────────────────────────────────────────────────────
    cell_size: float = 1.0
    cell_gap: float = 0.06
    cell_edgecolor: str = "none"
    cell_edgewidth: float = 0.0
    cell_rounding: float = 0.0

    # ── Colormap ─────────────────────────────────────────────────
    cmap: str = "RdBu_r"
    vmin: Optional[float] = None
    vmax: Optional[float] = None

    # ── Colorbar ─────────────────────────────────────────────────
    show_colorbar: bool = True
    colorbar_label: str = ""
    colorbar_width_frac: float = 0.08
    colorbar_pad: float = 0.5
    colorbar_fontsize: float = 9.0
    colorbar_tick_fontsize: float = 8.0

    # ── Row / col labels ─────────────────────────────────────────
    row_label_fontsize: float = 9.0
    col_label_fontsize: float = 10.0
    col_label_rotation: float = 90.0
    col_label_ha: str = "center"
    row_label_color: str = "#222222"
    col_label_color: str = "#222222"
    col_label_fontweight: str = "semibold"
    row_label_pad: float = 4.0
    col_label_pad: float = 4.0

    # ── Title / subtitle ─────────────────────────────────────────
    title_fontsize: float = 13.0
    title_fontweight: str = "bold"
    title_color: str = "#111111"
    title_pad: float = 10.0
    subtitle_fontsize: float = 10.0
    subtitle_color: str = "#555555"

    # ── Background ───────────────────────────────────────────────
    fig_facecolor: str = "#FFFFFF"
    ax_facecolor: str = "#FFFFFF"

    # ── Cell value annotation ────────────────────────────────────
    annotate: bool = False
    annotate_fontsize: float = 7.0
    annotate_fmt: str = "{:.1f}"
    annotate_color_threshold: float = 0.5

    # ── Significance markers ─────────────────────────────────────
    sig_marker: str = "*"
    sig_marker_fontsize: float = 8.0
    sig_marker_color: str = "#111111"

    # ── Axis spine ───────────────────────────────────────────────
    spine_color: str = "#444444"

    # ── Grid layout sizing ───────────────────────────────────────
    grid_row_label_width: float = 3.5
    grid_title_height: float = 1.2
    grid_col_label_height: float = 1.0
    grid_pad: float = 2.0
    grid_suptitle_y: Optional[float] = None


default_style = Style()
