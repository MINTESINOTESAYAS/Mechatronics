# Five-degree-of-freedom 3D printer thesis draft

- `main.tex`: complete, editable LaTeX proposal, including equations, tables, citations and references.
- `figures/`: the four conceptual schematics used by the LaTeX source; `generate_figures.py` can regenerate them.
- `5_DOF_3D_Printer_Thesis.pdf`: formatted proposal generated from the Markdown/Typst workflow.
- `5_DOF_3D_Printer_Thesis.docx`: editable Word version, including editable equations and embedded figures.
- `thesis.md`: source text, equations and references for the Markdown/Typst and Word workflow.

The institution on the title page follows the supplied example. Replace it if necessary, and fill in the student names, IDs, advisor and date. The design values are illustrative targets, not measured results. A completed thesis should add the actual CAD/FEA, experiment data, results, discussion and final conclusions after the research is performed.

## Edit and compile the LaTeX proposal

`main.tex` is a self-contained LaTeX document, with the exception of the four image files in `figures/`. Keep that folder next to `main.tex`. Edit the title-page commands near the top of the file to enter the author, advisor, date and institution. The nine references are written directly in the document's `thebibliography` environment; no `.bib` file or BibTeX run is required.

**Overleaf:** Start a new project from a ZIP containing `main.tex` and the `figures/` folder, or upload them to a blank project. Set `main.tex` as the main file and use the pdfLaTeX compiler.

**Local TeX installation:** From this directory, run pdfLaTeX twice so that citations and links resolve:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Alternatively, `latexmk -pdf main.tex` runs the necessary passes. The packages used are standard TeX Live/MiKTeX packages: `geometry`, `amsmath`, `amssymb`, `graphicx`, `float`, `titlesec`, `needspace`, `longtable`, `booktabs`, `array`, `calc`, `url` and `hyperref`. The generated `main.pdf` and auxiliary files are ignored by Git.

The LaTeX source and `thesis.md` are separate editable versions. Changes to one are not automatically applied to the other, and the original `build_thesis.py` does not regenerate `main.tex`.

## Rebuild the Markdown/Typst and Word versions

The original build uses Python 3, Pandoc, Typst, python-docx and Pillow. One way to install the tools is:

```sh
python -m pip install pypandoc-binary typst python-docx Pillow
python build_thesis.py
```

The schematic generator uses the DejaVu Sans fonts at `/usr/share/fonts/truetype/dejavu/`; adjust `FONT` and `BOLD` in `generate_figures.py` if they are installed elsewhere. The PDF title page is defined in `template.typst` and the Word title page in `add_title_page()` in `build_thesis.py`; change both if regenerating those documents with new personal details. Editing the Word document directly does not update the Markdown source, LaTeX source or PDF.
