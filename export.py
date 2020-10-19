"""This is a module to export data as PDF
"""

import os.path as path
from data_helper import get_dataframe
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.i pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm

# Register fonts
registerFont(TTFont('Arial', 'ARIAL.ttf'))
registerFont(TTFont('Arial-Bold', 'ARIAL BOLD.ttf'))
# Declare constant variables
CONST_PDF_PATH = 'resources/summary.pdf'
CONST_BARGRAPH_PATH = 'resources/bargraph.png'
CONST_TREEMAP_PATH = 'resources/treemap.png'


def setup_data_summary_page(pdf):
    """Function to set up data summary page
    Load filtered data and display it in a page in the pdf

    Parameters:
    pdf (canvas): canvas object for pdf document
    """
    # Retrieve data
    df = get_dataframe().head(1000)
    data = [df.columns.values.tolist()] + df.values.tolist()
    data[0] = list(map(lambda col_name: col_name.upper().replace('_', ' '), data[0]))

    # Page heading configurations
    pdf.setFont('Arial-Bold', 20, None)
    pdf.drawCentredString(415, 550, "Data Summary")

    # Format each text to allow word wrapping
    pstyle = ParagraphStyle(name='BodyText', fontName='Arial', fontSize=6, wordWrap='CJK')
    pcol_style = ParagraphStyle(name='BodyText', fontName='Arial-Bold', fontSize=8, wordWrap='CJK')
    data2 = [[Paragraph(str(row), pcol_style) for row in data[0]]] + \
            [[Paragraph(str(cell), pstyle) for cell in row] for row in data[1:]]

    # Table configurations
    col_widths = [50, 50, 70, 50, 60, 50, 100, 50, 40, 80, 50, 50, 50]
    table_styles = [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]
    x = 15
    y = 50
    width, height = A4
    data_count = len(data2)
    # If data is 20 or less, insert table to one page only
    # 21 because first how is header row
    if data_count <= 21:
        # Create table
        t = Table(data2, colWidths=col_widths)
        t.setStyle(TableStyle(table_styles))
        t.wrapOn(pdf, width, height)
        t.drawOn(pdf, x, y)
        pdf.showPage()
    # If more than 20 data
    else:
        index = 0
        end_index = 0
        rows_per_page = 30
        while not data_count <= 0:
            # Add 21 rows to first page (inclusive of header)
            if index == 0:
                data3 = data2[:21]
                index += 21
                end_index = index + rows_per_page
                data_count -= 21
            # Add 20 rows to subsequent pages
            else:
                if data_count > rows_per_page:
                    y = 30
                    data3 = data2[index:end_index]
                else:
                    y = 80
                    data3 = data2[index:]
                index = end_index
                end_index = index + rows_per_page
                data_count -= rows_per_page
            # Create table
            t = Table(data3, colWidths=col_widths)
            t.setStyle(TableStyle(table_styles))
            t.wrapOn(pdf, width, height)
            t.drawOn(pdf, x, y)
            pdf.showPage()


def setup_bargraph_page(pdf):
    """Function to set up bar graph page
    Inserts the bar graph image into the pdf

    Parameters:
    pdf (canvas): canvas object for pdf document
    """
    # Page heading configurations
    pdf.setFont('Arial-Bold', 20, None)
    pdf.drawCentredString(415, 550, "Bar Graph")
    # Insert bar graph image
    if path.isfile(CONST_BARGRAPH_PATH):
        pdf.drawImage(CONST_BARGRAPH_PATH, x=18, y=280, width=26 * cm, height=7 * cm)
    pdf.showPage()


def setup_treemap_page(pdf):
    """Function to set up tree map page
    Inserts the tree map image into the pdf

    Parameters:
    pdf (canvas): canvas object for pdf document
    """
    # Page heading configurations
    pdf.setFont('Arial-Bold', 20, None)
    pdf.drawCentredString(415, 550, "Tree Map")
    # Insert treemap image
    if path.isfile(CONST_TREEMAP_PATH):
        pdf.drawImage(CONST_TREEMAP_PATH, x=25, y=50, width=24 * cm, height=17 * cm)
    pdf.showPage()


def export_to_pdf():
    """Function to export summary data to PDF
    Page 1: Data summary table
    Page 2: Bar graph
    Page 3: Tree map
    """
    try:
        pdf = canvas.Canvas(CONST_PDF_PATH, pagesize=landscape(letter))
        setup_bargraph_page(pdf)
        setup_treemap_page(pdf)
        setup_data_summary_page(pdf)
        pdf.save()
    except Exception as e:
        print(e)


export_to_pdf()
