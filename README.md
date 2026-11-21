# mypaperfig

Matplotlib figures that drop into a MyPaper document at exactly 100 %: the right width,
the paper's font size, and (with LaTeX installed) the paper's own font for every label.

The layouts are copied from `style/MyPaperVersions.tex` in MyTemplate. When a version's
size, font or geometry changes there, change `VERSIONS` in `src/mypaperfig/__init__.py`.

## Install into a project

In the project folder:

```bash
uv add git+https://github.com/dnllcc/mypaperfig
```

After a change to this repository, update a project with:

```bash
uv sync --upgrade-package mypaperfig
```

## Use

```python
import matplotlib.pyplot as plt
import mypaperfig as mpf

mpf.use(version=2)                              # the number from \def\version{..} in paper.tex
fig, ax = plt.subplots(figsize=mpf.size(1.0))   # 1.0 full text width, 0.5 half
ax.plot(...)
fig.savefig("oscillator.pdf")
```

In the paper:

```latex
\myfigure{oscillator}{Damped oscillator, fig:osc}{}                         % size(1.0)
\myfigure{oscillator}{Damped oscillator, fig:osc}{}[width=0.5\linewidth]    % size(0.5)
```

`\myfigure` stretches every picture to the line width, so a figure made with `size(w)`
needs `[width=w\linewidth]` unless `w = 1`.

Options:

| Call | Meaning |
| --- | --- |
| `mpf.use(version=8)` | sizes and font of MyPaper version 8 |
| `mpf.use(version=2, font="times")` | override the font, as `\paperoptions{font=..}` |
| `mpf.use(version=2, latex=False)` | matplotlib's own maths instead of LaTeX |
| `mpf.use(version=2, preamble=r"\newcommand{\R}{\mathcal{R}}")` | extra LaTeX for labels |
| `mpf.size(0.5, ratio=1)` | half width, square |
| `mpf.size(1.0, wide=True)` | two-column versions (7, 9): across both columns |

## The version in the file name

`mpf.name("oscillator")` gives `oscillator-v8.pdf` after `mpf.use(version=8)`, so figures
made for different versions sit side by side instead of overwriting each other:

```python
fig.savefig(FIGURES / mpf.name("oscillator"))
```

In the paper, let `\version` choose the file, so switching the version line in
`paper.tex` also switches the figures:

```latex
\myfigure{oscillator-v\version}{Damped oscillator, fig:osc}{}
```

To make the figures for several versions in one run, loop over them:

```python
for v in [2, 8]:
    mpf.use(version=v)
    fig_oscillator()
```

`mpf.current_version()` returns the version set by the last `use()`.

## Versions

| Version | Layout | Width | Size | Font |
| --- | --- | --- | --- | --- |
| 0, 1, 2, P | editing, proofreading, arXiv, print | 15.5 cm | 11 pt | Latin Modern |
| 3, 13 | JHEP | 15 cm | 11 pt | Latin Modern |
| 4, 14 | SciPost | 16 cm | 11 pt | Latin Modern |
| 5 | Nucl. Phys. B | 15 cm | 12 pt | Latin Modern |
| 6 | J. Phys. A | 14 cm | 12 pt | Times |
| 7, 9, 17, 19 | Phys. Rev. D / Lett. | 3.375 in column (7 in page) | 10 pt | Times |
| 8 | Lett. Math. Phys. / Commun. Math. Phys. | 12.6 cm | 10 pt | Times |

With LaTeX (MacTeX) installed, labels are typeset by LaTeX; otherwise a look-alike font
is used. Labels are `\small`, tick labels and legends `\footnotesize`.
