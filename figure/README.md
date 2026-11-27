# LaTeX tables and figures for the survey

`build_figures.py` generates LaTeX tables and pgfplots figures from `data/papers.tsv`, ready to use in the survey. Rerun it whenever the data grows; do not edit the generated files.

```bash
python3 figure/build_figures.py                      # read data/papers.tsv
python3 figure/build_figures.py --pdf                # also compile PDFs (needs latexmk and xelatex from TeX Live)
python3 figure/build_figures.py --status confirmed   # count confirmed papers only
python3 figure/build_figures.py --data data/local/unconfirmed-papers.tsv --pdf
                                                     # preview the layout with local draft data (not for the paper)
```

Output goes to `figure/generated/`: the `.tex` sources at the top level, the PDFs from `--pdf` in `pdf/`, and intermediate LaTeX files in `build/`. The whole of `figure/generated/` is in `.gitignore`, so statistics computed from draft data are never committed by accident. Use `--out` to write straight into your paper's directory.

Data files still written in the old Chinese vocabulary (such as local drafts) are converted to the English values on the fly; see `scripts/migrate_to_english.py`.

## Generated files

| File | Contents | Label |
| --- | --- | --- |
| `rsi-macros.tex` | Colours, the heat-map cell macro, `\rsipaper`, and the pgfplots style. `\input` once in the preamble | — |
| `rsi-stats.tex` | Numbers to cite in the text: `\RSINumPapers`, `\RSINumConfirmed`, `\RSINumFullText`, `\RSINumRZero` … `\RSINumRFour`, `\RSINumDomainA` … `E` (domains 0–4), `\RSIYearRange` | — |
| `tab-levels.tex` | Self-reference depth levels R0–R4 and the number of papers at each | `tab:rsi-levels` |
| `tab-domain-depth.tex` | Heat-map table of domain × self-reference depth; the last row counts each paper once | `tab:rsi-domain-depth` |
| `tab-feedback-depth.tex` | Heat-map table of feedback source × self-reference depth | `tab:rsi-feedback-depth` |
| `tab-domain-feedback.tex` | Heat-map table of domain × feedback source | `tab:rsi-domain-feedback` |
| `fig-timeline.tex` | Papers per year of first release, stacked by self-reference depth | `fig:rsi-timeline` |
| `fig-loop.tex` | Loop automation by domain (horizontal stacked bars) | `fig:rsi-loop` |
| `tab-papers.tex` | All papers (`longtable`, for an appendix in a one-column layout) | `tab:rsi-papers` |
| `preview.tex` | A preview document with everything above | — |

An "Unclear" row or column is generated only when the data contains it. An R value that starts with R0–R4 (such as `R2 or R4 (unclear)`) is counted under its leading level.

## PDFs

With `--pdf`, `figure/generated/pdf/` contains:

- One single-page PDF per table and figure, cropped to its content, without caption or number, e.g. `tab-domain-depth.pdf` and `fig-timeline.pdf`. Include them with `\includegraphics` and write the caption in the paper.
- `tab-papers.pdf`: the full paper list, several pages.
- `preview.pdf`: everything together, with captions.

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\linewidth]{generated/pdf/fig-timeline.pdf}
  \caption{...}\label{fig:rsi-timeline}
\end{figure}
```

The PDFs are typeset at `\small`. Scaling them with `width=\linewidth` changes the font size accordingly; to match the body text exactly, include them at their natural size or `\input` the `.tex` source instead.

## Using the `.tex` sources directly

```latex
% preamble
\usepackage[table]{xcolor}       % \cellcolor for the heat maps
\usepackage{booktabs,longtable,array,graphicx}
\usepackage{pgfplots}\pgfplotsset{compat=1.18}
\usepackage{hyperref}            % optional: paper titles become links
\input{generated/rsi-macros.tex}
\input{generated/rsi-stats.tex}

% body
We collect \RSINumPapers{} papers (\RSIYearRange) ... see Table~\ref{tab:rsi-domain-depth}.
\input{generated/tab-domain-depth.tex}
\input{generated/fig-timeline.tex}
```

- XeLaTeX or LuaLaTeX is recommended; pdfLaTeX also works unless a paper title contains Unicode characters outside its font encoding.
- To add citations to the paper list, redefine `\rsipaper` after `\input{rsi-macros.tex}`, e.g. `\renewcommand{\rsipaper}[2]{#1}`.
- In a two-column template, tables and figures take one column by default. For full width, change `table`/`figure` to the starred form in the generated file, or set `wide=True` in `heat_table(...)` in the script.
- Captions, labels and colours are set in `TX` and `MACROS` in `build_figures.py`.
