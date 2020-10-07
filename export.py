"""This is a module to export data as PDF
"""
from fpdf import FPDF


def export_to_pdf():
    pdf = FPDF('L')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!', 1)
    pdf.cell(60, 10, 'Testing.', 0, 1, 'C')
    pdf.image('bargraph.png', x=None, y=None, w=0, h=0, type='', link='')
    pdf.output('test.pdf', 'F')

export_to_pdf()