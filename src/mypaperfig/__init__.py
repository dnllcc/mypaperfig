"""
mypaperfig: matplotlib figures that fit MyPaper without rescaling.

Usage (in any script or notebook of a project that has matplotlib):

    import matplotlib.pyplot as plt
    import mypaperfig as mpf

    mpf.use(version=2)                                   # same number as \\def\\version{..}
    fig, ax = plt.subplots(figsize=mpf.size(1.0))        # full text width
    ...
    fig.savefig("figures/oscillator.pdf")

and in the paper (the PDF lands at exactly 100 %):

    \\myfigure{oscillator}{Caption, fig:osc}{}                    % size(1.0)
    \\myfigure{oscillator}{Caption, fig:osc}{}[width=0.5\\linewidth]  % size(0.5)

\\myfigure scales a picture to fill \\linewidth, so a figure made with size(w) needs
[width=w\\linewidth] unless w = 1. In a two-column version (7, 9), size(1.0) is one
column; use size(1.0, wide=True) for a figure across both columns (\\myfigure*).

With LaTeX installed (MacTeX), all text is typeset by LaTeX in the paper's font.
Without it, matplotlib's own maths typesetting is used in a look-alike font.

The numbers below are copied from style/MyPaperVersions.tex in MyTemplate.
If a version's size, font or geometry changes there, change it here too.
"""

import os
import shutil

import matplotlib as mpl

PT_PER_INCH = 72.27  # TeX points
CM = 1 / 2.54        # inches per cm

# version: (text width in inches, column width in inches or None, font size in pt, font)
VERSIONS = {
    "0": (15.5 * CM, None, 11, "cm"),       # editing
    "1": (15.5 * CM, None, 11, "cm"),       # proofreading
    "2": (15.5 * CM, None, 11, "cm"),       # preprint (arXiv)
    "P": (15.5 * CM, None, 11, "cm"),       # print
    "3": (15.0 * CM, None, 11, "cm"),       # JHEP
    "4": (16.0 * CM, None, 11, "cm"),       # SciPost (A4, 2.5 cm margins)
    "5": (15.0 * CM, None, 12, "cm"),       # Nuclear Physics B
    "6": (14.0 * CM, None, 12, "times"),    # J. Phys. A
    "7": (7.0, 3.375, 10, "times"),         # Phys. Rev. D (letter, 0.75in margins, 0.25in gap)
    "8": (12.6 * CM, None, 10, "times"),    # Lett. Math. Phys. / Commun. Math. Phys.
    "9": (7.0, 3.375, 10, "times"),         # Phys. Rev. Lett.
}
# the journals' own classes: same sizes as their look-alikes
VERSIONS.update({"13": VERSIONS["3"], "14": VERSIONS["4"],
                 "17": VERSIONS["7"], "19": VERSIONS["9"]})

# LaTeX's \small and \footnotesize for each base size
SMALL = {10: 9.0, 11: 10.0, 12: 10.95}
FOOTNOTE = {10: 8.0, 11: 9.0, 12: 10.0}

PREAMBLE = {
    "cm": r"\usepackage{lmodern}\usepackage{amsmath}\usepackage{amssymb}\usepackage{bm}",
    "times": r"\usepackage{amsmath}\usepackage{newtxtext}\usepackage{newtxmath}\usepackage{bm}",
    "palatino": r"\usepackage{mathpazo}\usepackage{amsmath}\usepackage{amssymb}\usepackage{bm}",
}

_current = {"version": "2", "font": "cm"}


def _find_latex():
    """True if a LaTeX installation can be found (also when VS Code hides MacTeX's folder)."""
    texbin = "/Library/TeX/texbin"  # where MacTeX puts its programs
    if os.path.isdir(texbin) and texbin not in os.environ.get("PATH", "").split(os.pathsep):
        os.environ["PATH"] = texbin + os.pathsep + os.environ.get("PATH", "")
    return shutil.which("latex") is not None


def use(version=2, font=None, latex=None, preamble=""):
    """Set matplotlib up for a MyPaper version.

    version   the number (or "P") from \\def\\version{..} in paper.tex
    font      override the version's font: "cm", "times" or "palatino"
              (as \\paperoptions{font=..} in setup.tex)
    latex     True/False to force LaTeX on or off; default: on if LaTeX is installed
    preamble  extra LaTeX for the labels, e.g. r"\\newcommand{\\R}{\\mathcal{R}}"
    """
    version = str(version)
    if version not in VERSIONS:
        raise ValueError(f"unknown MyPaper version {version!r}; known: {', '.join(VERSIONS)}")
    _, _, size, version_font = VERSIONS[version]
    font = font or version_font
    if font not in PREAMBLE:
        raise ValueError("font must be 'cm', 'times' or 'palatino'")
    if latex is None:
        latex = _find_latex()

    mpl.rcdefaults()
    rc = {
        # sizes as in the text: labels \small, ticks and legend \footnotesize
        "font.size": size,
        "axes.labelsize": SMALL[size],
        "axes.titlesize": size,
        "xtick.labelsize": FOOTNOTE[size],
        "ytick.labelsize": FOOTNOTE[size],
        "legend.fontsize": FOOTNOTE[size],
        # lines matched to text this size
        "lines.linewidth": 1.0,
        "lines.markersize": 3.5,
        "axes.linewidth": 0.6,
        "grid.linewidth": 0.4,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6,
        "xtick.minor.width": 0.4, "ytick.minor.width": 0.4,
        "xtick.major.size": 3.5, "ytick.major.size": 3.5,
        "xtick.minor.size": 2.0, "ytick.minor.size": 2.0,
        "xtick.direction": "in", "ytick.direction": "in",
        "xtick.top": True, "ytick.right": True,
        "legend.frameon": False,
        # the saved file has exactly the size given to the figure
        "figure.constrained_layout.use": True,
        "savefig.bbox": "standard",
        "savefig.format": "pdf",
        "savefig.dpi": 300,
        "pdf.fonttype": 42,
    }
    if latex:
        rc.update({
            "text.usetex": True,
            "font.family": "serif",
            "text.latex.preamble": PREAMBLE[font] + preamble,
        })
    else:
        rc.update({
            "text.usetex": False,
            "font.family": "serif",
            "font.serif": ["CMU Serif", "Latin Modern Roman", "DejaVu Serif"] if font == "cm"
                          else ["Times New Roman", "Times", "STIXGeneral", "DejaVu Serif"],
            "mathtext.fontset": "cm" if font == "cm" else "stix",
            "axes.formatter.use_mathtext": True,
        })
    mpl.rcParams.update(rc)
    _current.update(version=version, font=font)
    return latex


def size(width=1.0, ratio=None, height=None, wide=False):
    """Figure size (inches) for plt.subplots(figsize=...).

    width   fraction of the text (one column in two-column versions): 1.0 full, 0.5 half
    ratio   height / width; default the golden ratio 0.618
    height  height as a fraction of the width of the full text, instead of ratio
    wide    two-column versions only: across both columns (\\myfigure*)
    """
    textwidth, columnwidth, _, _ = VERSIONS[_current["version"]]
    full = textwidth if (wide or columnwidth is None) else columnwidth
    w = width * full
    if height is not None:
        h = height * full
    else:
        h = w * (ratio if ratio is not None else (5 ** 0.5 - 1) / 2)
    return (w, h)


def textwidth_pt():
    """Width of size(1.0) in TeX points, to compare with \\the\\linewidth in the paper."""
    return size(1.0)[0] * PT_PER_INCH


def current_version():
    """The MyPaper version set by the last use(), as a string ("2", "8", "P", ...)."""
    return _current["version"]


def name(base, ext="pdf"):
    """File name with the MyPaper version in it: name("oscillator") -> "oscillator-v8.pdf".

    In the paper, \\myfigure{oscillator-v\\version}{..}{} then picks the figure made for
    the version that paper.tex is set to.
    """
    return f"{base}-v{_current['version']}.{ext}"
