"""Tests for Style configuration."""

from cubeheatmap.style import (
    Style,
    default_style,
)


class TestStyleDefaults:

    def test_default_style_is_style(self):
        assert isinstance(default_style, Style)

    def test_default_cell_size(self):
        assert default_style.cell_size == 1.0

    def test_default_cmap(self):
        assert default_style.cmap == "RdBu_r"

    def test_default_annotate_false(self):
        assert default_style.annotate is False

    def test_default_colorbar_true(self):
        assert default_style.show_colorbar is True

    def test_default_rounding_zero(self):
        assert default_style.cell_rounding == 0.0

    def test_default_label_colors(self):
        assert default_style.row_label_color == "#222222"
        assert default_style.col_label_color == "#222222"


class TestStyleCustom:

    def test_override_specific(self):
        s = Style(cmap="Blues", cell_size=0.5)
        assert s.cmap == "Blues"
        assert s.cell_size == 0.5
        assert s.annotate is False  # unchanged

    def test_all_params_settable(self):
        s = Style(
            cell_size=0.8,
            cell_gap=0.1,
            cell_edgecolor="black",
            cell_edgewidth=1.0,
            cell_rounding=0.2,
            cmap="viridis",
            vmin=-1,
            vmax=1,
            show_colorbar=False,
            colorbar_label="test",
            colorbar_width_frac=0.1,
            colorbar_pad=0.6,
            colorbar_fontsize=10.0,
            colorbar_tick_fontsize=9.0,
            row_label_fontsize=8.0,
            col_label_fontsize=9.0,
            col_label_rotation=45.0,
            col_label_ha="right",
            row_label_color="red",
            col_label_color="blue",
            col_label_fontweight="bold",
            row_label_pad=5.0,
            col_label_pad=5.0,
            title_fontsize=14.0,
            title_fontweight="normal",
            title_color="green",
            title_pad=12.0,
            subtitle_fontsize=11.0,
            subtitle_color="gray",
            fig_facecolor="#000000",
            ax_facecolor="#111111",
            annotate=True,
            annotate_fontsize=9.0,
            annotate_fmt="{:.2f}",
            annotate_color_threshold=0.6,
            sig_marker="+",
            sig_marker_fontsize=10.0,
            sig_marker_color="red",
            spine_color="black",
            grid_row_label_width=4.0,
            grid_title_height=1.5,
            grid_col_label_height=1.2,
            grid_pad=2.5,
            grid_suptitle_y=0.95,
        )
        assert s.cmap == "viridis"
        assert s.fig_facecolor == "#000000"
        assert s.annotate is True

    def test_dark_theme(self):
        dark = Style(
            fig_facecolor="#1A1A2E",
            ax_facecolor="#1A1A2E",
            row_label_color="#CCCCCC",
            col_label_color="#CCCCCC",
            title_color="#EEEEEE",
        )
        assert dark.fig_facecolor.startswith("#")
