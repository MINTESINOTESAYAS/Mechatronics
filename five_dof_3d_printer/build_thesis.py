#!/usr/bin/env python3
"""Build the thesis proposal PDF and editable Word document from thesis.md.

Install dependencies: python -m pip install pypandoc-binary typst python-docx Pillow
Run: python build_thesis.py
The institution and personal-information fields intentionally remain editable
placeholders. The PDF title page is defined in template.typst; the Word title
page is defined in add_title_page below.
"""
from pathlib import Path
import subprocess
import sys
import tempfile

import pypandoc
import typst
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = Path(__file__).resolve().parent
MD = HERE / 'thesis.md'
PDF = HERE / '5_DOF_3D_Printer_Thesis.pdf'
DOCX = HERE / '5_DOF_3D_Printer_Thesis.docx'
PANDOC = pypandoc.get_pandoc_path()


def run(*args):
    subprocess.run([str(x) for x in args], cwd=HERE, check=True)


def style_doc(doc):
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.5)
    sec.top_margin = sec.bottom_margin = Cm(2.5)
    sec.different_first_page_header_footer = True
    # The title page is physically page zero, so the abstract reads page 1.
    sect_pr = sec._sectPr
    pg_num = sect_pr.find(qn('w:pgNumType'))
    if pg_num is None:
        pg_num = OxmlElement('w:pgNumType')
        sect_pr.append(pg_num)
    pg_num.set(qn('w:start'), '0')
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), 'PAGE')
    footer._p.append(fld)

    # Pandoc distinguishes the first paragraph and normal body paragraphs.
    for name in ('Normal', 'Body Text', 'First Paragraph', 'Compact'):
        st = doc.styles[name]
        st.font.name = 'Times New Roman'
        st.font.size = Pt(12)
        st.font.color.rgb = RGBColor.from_string('000000')
        st.paragraph_format.line_spacing = 1.15
        st.paragraph_format.space_after = Pt(6)
        if name != 'Compact':
            st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    for name, size in (('Heading 1', 15), ('Heading 2', 13), ('Heading 3', 12)):
        st = doc.styles[name]
        st.font.name = 'Times New Roman'
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = RGBColor.from_string('000000')
        st.paragraph_format.space_before = Pt(8)
        st.paragraph_format.space_after = Pt(4)
        st.paragraph_format.keep_with_next = True
        st.paragraph_format.page_break_before = (name == 'Heading 1')
    for name in ('Table Caption', 'Image Caption'):
        st = doc.styles[name]
        st.font.name = 'Times New Roman'
        st.font.size = Pt(10)
        st.font.color.rgb = RGBColor.from_string('000000')
        st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        st.paragraph_format.space_after = Pt(5)
        st.paragraph_format.keep_with_next = (name == 'Table Caption')
    if 'Captioned Figure' in doc.styles:
        doc.styles['Captioned Figure'].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.styles['Captioned Figure'].paragraph_format.keep_with_next = True

    # Percentages mirror the table column proportions in the Markdown source.
    table_widths = [
        (0.35, 0.10, 0.183, 0.183, 0.184),
        (0.29, 0.71),
        (0.29, 0.71),
        (0.23, 0.42, 0.35),
        (0.18, 0.47, 0.35),
    ]
    assert len(doc.tables) == len(table_widths), 'Review table widths after editing the source.'
    for table, widths in zip(doc.tables, table_widths):
        # Pandoc's reference document may not include the Word 'Table Grid'
        # style, so define the borders directly instead of relying on it.
        tbl_pr = table._tbl.tblPr
        borders = tbl_pr.find(qn('w:tblBorders'))
        if borders is None:
            borders = OxmlElement('w:tblBorders')
            tbl_pr.append(borders)
        for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
            line = borders.find(qn('w:' + edge))
            if line is None:
                line = OxmlElement('w:' + edge)
                borders.append(line)
            line.set(qn('w:val'), 'single')
            line.set(qn('w:sz'), '4')
            line.set(qn('w:color'), 'AAB4BA')
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        for col, frac in zip(table.columns, widths):
            col.width = Cm(16 * frac)
        for row_index, row in enumerate(table.rows):
            tr_pr = row._tr.get_or_add_trPr()
            tr_pr.append(OxmlElement('w:cantSplit'))
            if row_index == 0:
                tr_pr.append(OxmlElement('w:tblHeader'))
            for cell, frac in zip(row.cells, widths):
                cell.width = Cm(16 * frac)
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                if row_index == 0:
                    shade = OxmlElement('w:shd')
                    shade.set(qn('w:fill'), 'EDF2F4')
                    cell._tc.get_or_add_tcPr().append(shade)
                for para in cell.paragraphs:
                    para.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    para.paragraph_format.line_spacing = 1.0
                    para.paragraph_format.space_after = Pt(0)
                    for r in para.runs:
                        r.font.name = 'Times New Roman'
                        r.font.size = Pt(10)
                        if row_index == 0:
                            r.bold = True

    doc.core_properties.title = 'Design and Development of a Five-Degree-of-Freedom 3D Printer'
    doc.core_properties.subject = 'Mechatronics thesis proposal draft'
    doc.core_properties.author = ''


def add_title_page(doc):
    first = doc.element.body[0]
    def add(text, *, size=12, bold=False, italic=False, before=0, after=0):
        p = doc.add_paragraph()
        first.addprevious(p._p)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_before = Pt(before)
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.keep_with_next = False
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        run.bold, run.italic = bold, italic
        return p
    add('Design and Development of a\nFive-Degree-of-Freedom 3D Printer', size=18, bold=True, before=28, after=40)
    add('A Design of Mechatronics Thesis Proposal Submitted\nto the Department of Electromechanical Engineering', after=30)
    add('College of Engineering\nAddis Ababa Science and Technology University', bold=True, after=43)
    add('By', bold=True, after=18)
    add('[Student Name(s) and ID Number(s)]', after=43)
    add('Advisor: [Advisor Name]', after=35)
    add('Proposal draft: design targets and calculations are preliminary;\nexperimental results are not yet available.', size=10.5, italic=True, after=0)
    add('[Month Year]\nAddis Ababa, Ethiopia', before=115)


def main():
    run(sys.executable, HERE / 'generate_figures.py')
    # Typst requires the source to be within the project root for image access.
    with tempfile.NamedTemporaryFile(mode='w', suffix='.typ', prefix='.thesis_', dir=HERE, delete=False) as t:
        typ_path = Path(t.name)
    try:
        run(PANDOC, MD, '-f', 'markdown+tex_math_dollars', '-t', 'typst',
            '--template', HERE / 'template.typst', '-o', typ_path)
        _, warnings = typst.compile_with_warnings(str(typ_path), root=str(HERE), output=str(PDF))
        if warnings:
            for warning in warnings:
                print('Typst warning:', warning, file=sys.stderr)
    finally:
        typ_path.unlink(missing_ok=True)

    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as t:
        tmp_docx = Path(t.name)
    try:
        run(PANDOC, MD, '-f', 'markdown+tex_math_dollars', '-o', tmp_docx,
            '--resource-path', HERE)
        doc = Document(tmp_docx)
        style_doc(doc)
        add_title_page(doc)
        doc.save(DOCX)
    finally:
        tmp_docx.unlink(missing_ok=True)
    print(f'Wrote {PDF.name} and {DOCX.name}')


if __name__ == '__main__':
    main()
