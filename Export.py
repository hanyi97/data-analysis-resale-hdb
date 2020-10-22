"""This is a module to export data as PDF
"""

import os.path as path
from Filter import get_filtered_data, get_cheapest_hdb
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm

# Declare constant variables
CONST_PDF_PATH = 'resources/summary.pdf'
CONS_CSV_PATH = 'resources/summary.csv'
CONST_BARGRAPH_PATH = 'resources/bargraph.png'
CONST_TREEMAP_PATH = 'resources/treemap.png'
# Declare style for page headings
heading_style = getSampleStyleSheet()['Heading1']
heading_style.alignment = 1
heading_style.leading = 30


def setup_data_summary_page():
    """Function to set up data summary page
    Load filtered data and display it in a page in the pdf
    """
    # Retrieve data
    df = get_cheapest_hdb()
    if len(df) == 0:
        return []

    # Format data
    data = [df.columns.values.tolist()] + df.values.tolist()
    data[0] = list(map(lambda col_name: '<b>'+col_name.upper().replace('_', ' ') + '</b>', data[0]))

    # Create a list and add heading to list
    elements = [Paragraph("<u>Cheapest Flats</u>", heading_style)]

    # Format each text to allow word wrapping
    pcol_style = ParagraphStyle(name='BodyText', fontSize=8, wordWrap='CJK')
    pstyle = ParagraphStyle(name='BodyText', fontSize=8, wordWrap='CJK')
    data2 = [[Paragraph(str(row), pcol_style) for row in data[0]]] + \
            [[Paragraph(str(cell), pstyle) for cell in row] for row in data[1:]]

    # Table configurations
    col_widths = [50, 50, 70, 50, 60, 50, 100, 50, 40, 80, 50, 50, 50]
    table_styles = [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]

    # Create table
    table = Table(data2, colWidths=col_widths)
    table.setStyle(TableStyle(table_styles))
    elements.append(table)
    elements.append(PageBreak())
    return elements


def setup_bargraph_page():
    """Function to set up bar graph page
    Inserts the bar graph image into the pdf
    """
    elements = []
    if path.isfile(CONST_BARGRAPH_PATH):
        elements.append(Paragraph('<u>Bar Graph</u>', heading_style))
        elements.append(Image(CONST_BARGRAPH_PATH, width=26 * cm, height=7 * cm))
        elements.append(PageBreak())
    return elements


def setup_treemap_page():
    """Function to set up tree map page
    Inserts the tree map image into the pdf
    """
    elements = []
    if path.isfile(CONST_TREEMAP_PATH):
        elements.append(Paragraph('<u>Tree Map</u>', heading_style))
        elements.append(Image(CONST_TREEMAP_PATH, width=19 * cm, height=14 * cm))
        elements.append(PageBreak())
    return elements


def export_to_pdf(file_path=CONST_PDF_PATH):
    """Function to export summary data to PDF
    Page 1: Bar graph
    Page 2: Tree map
    Page 3: Cheapest flat table
    """
    try:
        pdf = SimpleDocTemplate(file_path, pagesize=landscape(A4))
        pdf.build(setup_bargraph_page() +
                  setup_treemap_page() +
                  setup_data_summary_page())
    except Exception as e:
        print(e)


def export_to_csv(file_path=CONS_CSV_PATH, filters={}):
    """Function to export filtered data to CSV
    Call get_filtered_data function from search module to retrieve user filtered data
    """
    df = get_filtered_data(filters)
    df.to_csv(file_path, index=False)

