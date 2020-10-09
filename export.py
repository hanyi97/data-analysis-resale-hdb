"""This is a module to export data as PDF
"""
from fpdf import FPDF


def export_to_pdf():
    pdf = FPDF('L')
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!', 1)
    pdf.cell(60, 10, 'Testing.', 0, 1, 'C')
    pdf.image('resources/bargraph.png', x=None, y=None, w=250, h=200, type='', link='')
    pdf.output('resources/test.pdf', 'F')


export_to_pdf()