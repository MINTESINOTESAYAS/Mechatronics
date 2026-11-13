# Five-degree-of-freedom 3D printer thesis draft

- `5_DOF_3D_Printer_Thesis.pdf`: formatted proposal, following the supplied example.
- `5_DOF_3D_Printer_Thesis.docx`: editable Word version, including editable equations and embedded figures.
- `thesis.md`: source text, equations and references.
- `figures/`: original conceptual schematics; `generate_figures.py` regenerates them.

The institution on the title page follows the supplied example. Replace it if necessary, and fill in the student names, IDs, advisor and date. The design values are illustrative targets, not measured results. A completed thesis should add the actual CAD/FEA, experiment data, results, discussion and final conclusions after the research is performed.

## Rebuilding

The build uses Python 3, Pandoc, Typst, python-docx and Pillow. One way to install the tools is:

```sh
python -m pip install pypandoc-binary typst python-docx Pillow
python build_thesis.py
```

The schematic generator uses the DejaVu Sans fonts at `/usr/share/fonts/truetype/dejavu/`; adjust `FONT` and `BOLD` in `generate_figures.py` if they are installed elsewhere. The PDF title page is defined in `template.typst` and the Word title page in `add_title_page()` in `build_thesis.py`; change both if regenerating the documents with new personal details. Editing the Word document directly does not update the Markdown source or the PDF.
