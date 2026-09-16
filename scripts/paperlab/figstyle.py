"""Shared ICLR publication style for paper figures.

Implements the Orchestra academic-plotting style guide, ICLR profile:
single-column 5.5in text width, vector PDF export, colorblind-safe Okabe-Ito
palette, one marker shape per family, no decorative elements. Import `setup()`
before creating any figure and use `save()` for dual PDF+PNG export.

Family colors are fixed across ALL paper figures:
  scaffold ART  -> black        generic transformer -> blue
  scaffold CNN  -> green        generic CNN        -> orange
  diffusion     -> vermillion
"""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ICLR_WIDTH = 5.5   # ICLR single-column full text width (inches)
HALF_WIDTH = 2.65  # half width, side-by-side
MAX_HEIGHT = 9.0

# Okabe-Ito colorblind-safe palette
OKABE_ITO = {
    "black": "#000000", "orange": "#E69F00", "sky": "#56B4E9",
    "green": "#009E73", "yellow": "#F0E442", "blue": "#0072B2",
    "vermillion": "#D55E00", "purple": "#CC79A7", "grey": "#999999",
}

FAMILY = {
    "scaffold_art": OKABE_ITO["black"],
    "scaffold_cnn": OKABE_ITO["green"],
    "gen_transformer": OKABE_ITO["blue"],
    "gen_cnn": OKABE_ITO["orange"],
    "gen_diffusion": OKABE_ITO["vermillion"],
}

FAMILY_MARKER = {
    "scaffold_art": "o", "scaffold_cnn": "s", "gen_transformer": "o",
    "gen_cnn": "^", "gen_diffusion": "D",
}


def setup():
    """Apply ICLR rcParams; call once before building figures."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 8.0,
        "axes.titlesize": 8.5, "axes.labelsize": 8.5,
        "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
        "legend.fontsize": 7.0, "legend.frameon": False,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "lines.linewidth": 1.3, "lines.markersize": 4.5,
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.width": 0.8, "ytick.major.width": 0.8,
        "pdf.fonttype": 42,        # TrueType: text stays editable in PDF
        "savefig.dpi": 300,
        "axes.grid": False,
    })


def save(fig, name, figs_dir="docs/figs/paper"):
    """Write <figs_dir>/<name>.pdf (vector, for LaTeX) and .png (300dpi preview)."""
    out = Path(figs_dir)
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(out / f"{name}.png", bbox_inches="tight")
    return out / f"{name}.pdf", out / f"{name}.png"
