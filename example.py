"""cubeheatmap demo — run this to generate example plots."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import cubeheatmap as ch

OUT = Path(__file__).parent / "example_output"
OUT.mkdir(exist_ok=True)

GENES = [
    "Il1b", "Tnf", "Cxcl10", "Ccr2", "S100a8", "Nos2",
    "Arg1", "Trem2", "Spp1", "Mrc1",
    "Lyve1", "Timd4", "Folr2", "Cd163", "Gpnmb",
]
TIMEPOINTS = ["Day14", "Day21", "Day40"]

rng = np.random.default_rng(42)


# ══════════════════════════════════════════════════════════════════
# 1. from_matrix — prosty przykład
# ══════════════════════════════════════════════════════════════════
print("1. from_matrix...")

matrix = rng.uniform(-4, 4, (len(GENES), len(TIMEPOINTS)))
hm1 = ch.CubeHeatmap.from_matrix(matrix, row_labels=GENES, col_labels=TIMEPOINTS)

style1 = ch.Style(
    cmap="RdBu_r",
    vmin=-4.0,
    vmax=4.0,
    colorbar_label="log2FC",
    cell_size=0.55,
    cell_gap=0.05,
)
ax1 = ch.draw(hm1, title="Macrophage DEG", subtitle="Day14 / Day21 / Day40 vs Day0", style=style1)
ax1.figure.savefig(OUT / "1_from_matrix.png", dpi=150, bbox_inches="tight")
plt.close(ax1.figure)
print(f"   -> {OUT / '1_from_matrix.png'}")


# ══════════════════════════════════════════════════════════════════
# 2. from_dataframe — pandas input
# ══════════════════════════════════════════════════════════════════
print("2. from_dataframe...")

df2 = pd.DataFrame(
    rng.uniform(-3, 3, (8, 4)),
    index=[f"Gene_{i}" for i in range(8)],
    columns=["Ctrl vs T1", "Ctrl vs T2", "Ctrl vs T3", "Ctrl vs T4"],
)
hm2 = ch.CubeHeatmap.from_dataframe(df2)
ax2 = ch.draw(hm2, title="from_dataframe()", style=ch.Style(cmap="coolwarm", vmin=-3, vmax=3,
                                                             colorbar_label="LFC",
                                                             col_label_rotation=30.0))
ax2.figure.savefig(OUT / "2_from_dataframe.png", dpi=150, bbox_inches="tight")
plt.close(ax2.figure)
print(f"   -> {OUT / '2_from_dataframe.png'}")


# ══════════════════════════════════════════════════════════════════
# 3. top_n_rows — automatyczny wybor najwazniejszych genow
# ══════════════════════════════════════════════════════════════════
print("3. top_n_rows...")

big_matrix = rng.uniform(-6, 6, (60, 3))
hm_big = ch.CubeHeatmap.from_matrix(
    big_matrix,
    row_labels=[f"Gene_{i:02d}" for i in range(60)],
    col_labels=TIMEPOINTS,
)
hm3 = hm_big.top_n_rows(20)
ax3 = ch.draw(hm3, title="Top 20 genes (max |LFC|)", style=ch.Style(
    cmap="RdBu_r", vmin=-6, vmax=6, colorbar_label="log2FC",
    row_label_fontsize=8.0, cell_size=0.5,
))
ax3.figure.savefig(OUT / "3_top_n.png", dpi=150, bbox_inches="tight")
plt.close(ax3.figure)
print(f"   -> {OUT / '3_top_n.png'}")


# ══════════════════════════════════════════════════════════════════
# 4. annotate — wartosci w komorkach
# ══════════════════════════════════════════════════════════════════
print("4. annotate...")

hm4 = ch.CubeHeatmap.from_matrix(
    rng.uniform(-2, 2, (6, 3)),
    row_labels=[f"Gene_{i}" for i in range(6)],
    col_labels=TIMEPOINTS,
)
ax4 = ch.draw(hm4, title="Annotated cells", style=ch.Style(
    cmap="RdBu_r", vmin=-2, vmax=2,
    annotate=True, annotate_fmt="{:.2f}",
    cell_size=0.8, colorbar_label="LFC",
))
ax4.figure.savefig(OUT / "4_annotated.png", dpi=150, bbox_inches="tight")
plt.close(ax4.figure)
print(f"   -> {OUT / '4_annotated.png'}")


# ══════════════════════════════════════════════════════════════════
# 5. sig_mask — gwiazki istotnosci
# ══════════════════════════════════════════════════════════════════
print("5. sig_mask...")

mat5 = rng.uniform(-4, 4, (10, 3))
mask5 = np.abs(mat5) > 2.5
hm5 = ch.CubeHeatmap.from_matrix(mat5, row_labels=[f"Gene_{i}" for i in range(10)],
                                  col_labels=TIMEPOINTS)
ax5 = ch.draw(hm5, title="With significance markers", style=ch.Style(
    cmap="RdBu_r", vmin=-4, vmax=4,
    colorbar_label="log2FC", sig_marker="*", sig_marker_fontsize=9.0,
), sig_mask=mask5)
ax5.figure.savefig(OUT / "5_sig_mask.png", dpi=150, bbox_inches="tight")
plt.close(ax5.figure)
print(f"   -> {OUT / '5_sig_mask.png'}")


# ══════════════════════════════════════════════════════════════════
# 6. draw_grid — kilka heatmap obok siebie
# ══════════════════════════════════════════════════════════════════
print("6. draw_grid...")

cell_types = ["T cell", "B cell", "NK cell", "Macrophage"]
heatmaps6 = [
    ch.CubeHeatmap.from_matrix(
        rng.uniform(-4, 4, (8, len(TIMEPOINTS))),
        row_labels=[f"Gene_{i}" for i in range(8)],
        col_labels=TIMEPOINTS,
    )
    for _ in cell_types
]
style6 = ch.Style(cmap="RdBu_r", vmin=-4, vmax=4, colorbar_label="log2FC",
                  cell_size=0.45, cell_gap=0.04, row_label_fontsize=7.5)
fig6 = ch.draw_grid(
    heatmaps6,
    titles=cell_types,
    suptitle="DEG LFC Heatmaps per cell type",
    ncols=2,
    style=style6,
)
fig6.savefig(OUT / "6_grid.png", dpi=150, bbox_inches="tight")
plt.close(fig6)
print(f"   -> {OUT / '6_grid.png'}")


# ══════════════════════════════════════════════════════════════════
# 7. cell_rounding — zaokraglone komorki
# ══════════════════════════════════════════════════════════════════
print("7. cell_rounding...")

hm7 = ch.CubeHeatmap.from_matrix(
    rng.uniform(-3, 3, (8, 3)),
    row_labels=[f"Gene_{i}" for i in range(8)],
    col_labels=TIMEPOINTS,
)
ax7 = ch.draw(hm7, title="Rounded corners", style=ch.Style(
    cmap="RdBu_r", vmin=-3, vmax=3,
    cell_rounding=0.15, cell_gap=0.10, colorbar_label="LFC",
))
ax7.figure.savefig(OUT / "7_rounded.png", dpi=150, bbox_inches="tight")
plt.close(ax7.figure)
print(f"   -> {OUT / '7_rounded.png'}")


# ══════════════════════════════════════════════════════════════════
# 8. custom Style — ciemne tlo
# ══════════════════════════════════════════════════════════════════
print("8. dark background...")

hm8 = ch.CubeHeatmap.from_matrix(
    rng.uniform(-5, 5, (12, 3)),
    row_labels=[f"Gene_{i:02d}" for i in range(12)],
    col_labels=TIMEPOINTS,
)
dark = ch.Style(
    cmap="RdBu_r", vmin=-5, vmax=5,
    fig_facecolor="#1A1A2E", ax_facecolor="#1A1A2E",
    row_label_color="#CCCCCC", col_label_color="#CCCCCC",
    title_color="#EEEEEE", colorbar_label="log2FC",
    colorbar_tick_fontsize=8.0, colorbar_fontsize=9.0,
    cell_gap=0.06,
)
ax8 = ch.draw(hm8, title="Dark theme", subtitle="12 genes x 3 timepoints", style=dark)
ax8.figure.savefig(OUT / "8_dark.png", dpi=150, bbox_inches="tight")
plt.close(ax8.figure)
print(f"   -> {OUT / '8_dark.png'}")


# ══════════════════════════════════════════════════════════════════
print()
print(f"Done! {len(list(OUT.glob('*.png')))} plots saved to {OUT}/")
for f in sorted(OUT.glob("*.png")):
    print(f"  {f.name}")
