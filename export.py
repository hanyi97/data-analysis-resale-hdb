"""This is a module to export data as PDF
"""
from fpdf import FPDF


def export_to_pdf():
    pdf = FPDF()
    pdf.add_page()