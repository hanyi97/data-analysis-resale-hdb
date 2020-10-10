"""This is a module to export data as PDF
"""
import data_helper
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
# Register fonts
registerFont(TTFont('Arial', 'ARIAL.ttf'))
registerFont(TTFont('Arial-Bold', 'ARIAL BOLD.ttf'))


def export_to_pdf():
    """Function to export summary data to PDF
    Page 1: Data summary table
    Page 2: Bar graph
    Page 3: Tree map
    """
    df = data_helper.get_dataframe().head(10)
    data = [df.columns.values.tolist()] + df.values.tolist()
    data[0] = list(map(lambda col_name: col_name.upper().replace('_', ' '), data[0]))

    # Data Summary page
    pdf = canvas.Canvas('resources/summary.pdf', pagesize=landscape(letter))
    pdf.setFont('Arial-Bold', 20, None)
    pdf.drawCentredString(415, 550, "Data Summary")
    # Table configurations
    style = ParagraphStyle(
        name='BodyText',
        fontName='Arial',
        fontSize=8,
        wordWrap='CJK'
    )
    col_style = ParagraphStyle(
        name='BodyText',
        fontName='Arial-Bold',
        fontSize=8,
        wordWrap='CJK'
    )
    data2 = [[Paragraph(str(row), col_style) for row in data[0]]] + \
            [[Paragraph(str(cell), style) for cell in row] for row in data[1:]]
    t = Table(data2, colWidths=[50, 50, 100, 50, 60, 50, 100, 50, 50, 50, 50, 50, 50])
    t.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ]))
    width, height = A4
    t.wrapOn(pdf, width, height)
    t.drawOn(pdf, 10, 250)
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


export_to_pdf()
