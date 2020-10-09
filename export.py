"""This is a module to export data as PDF
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
registerFont(TTFont('Arial', 'ARIAL.ttf'))
registerFont(TTFont('Arial-Bold', 'ARIAL BOLD.ttf'))


def export_to_pdf():
    pdf = canvas.Canvas('resources/summary.pdf', pagesize=landscape(letter))
    # Data summary page
    pdf.setFont('Arial-Bold', 20, None)
    pdf.drawCentredString(415, 550, "Data Summary")
    pdf.showPage()
    # Bar graph page
    pdf.setFont('Arial-Bold', 20, None)
    pdf.drawCentredString(415, 550, "Bar Graph")
    pdf.drawImage('resources/bargraph.png', x=55, y=120, width=650, height=400)
    pdf.showPage()
    # Tree map page
    pdf.setFont('Arial-Bold', 20, None)
    pdf.drawCentredString(415, 550, "Tree Map")
    pdf.showPage()
    pdf.save()
