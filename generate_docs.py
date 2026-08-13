import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# =====================================================================
# 1. SET AUTOMATIC DOWNLOADS PATH
# =====================================================================

# Automatically gets C:\Users\<YourName>\Downloads (Windows/Mac/Linux compatible)
DOWNLOADS_DIR = Path.home() / "Downloads"

pdf_path = str(DOWNLOADS_DIR / "mock_documents.pdf")
ar_img_path = str(DOWNLOADS_DIR / "invoices_ar.png")
ledger_img_path = str(DOWNLOADS_DIR / "financial_ledger.png")
bank_img_path = str(DOWNLOADS_DIR / "bank_statement.png")

# =====================================================================
# 2. MOCK DATASETS
# =====================================================================

ar_data = [
    ['Invoice_ID', 'Customer', 'Amount (₹)', 'Due_Date', 'Status', 'Risk_Score'],
    ['INV-2001', 'Vanguard Tech', '250,000', '2026-07-10', 'Overdue (30+ d)', 'HIGH'],
    ['INV-2002', 'Nexus Logistics', '180,000', '2026-07-25', 'Overdue (15 d)', 'HIGH'],
    ['INV-2003', 'Aether Systems', '120,000', '2026-08-02', 'Overdue (8 d)', 'MEDIUM'],
    ['INV-2004', 'Orion Industrial', '300,000', '2026-08-20', 'Current', 'LOW'],
    ['INV-2005', 'Zenith Auto', '150,000', '2026-09-05', 'Current', 'LOW']
]

ledger_data = [
    ['Month', 'Revenue (₹)', 'Expenses (₹)', 'Profit (₹)'],
    ['Mar 2026', '4,000,000', '2,800,000', '1,200,000'],
    ['Apr 2026', '4,200,000', '2,900,000', '1,300,000'],
    ['May 2026', '4,500,000', '3,100,000', '1,400,000'],
    ['Jun 2026', '4,400,000', '3,150,000', '1,250,000'],
    ['Jul 2026', '4,800,000', '3,360,000', '1,440,000'],
    ['Aug 2026', '5,000,000', '3,500,000', '1,500,000']
]

bank_data = [
    ['Date', 'Cash_Balance (₹)'],
    ['Jul 01', '2,500,000'],
    ['Jul 10', '2,400,000'],
    ['Jul 20', '2,300,000'],
    ['Jul 30', '2,150,000'],
    ['Aug 05', '2,050,000'],
    ['Aug 13', '2,000,000']
]


# =====================================================================
# 3. GENERATORS
# =====================================================================

def generate_pdf_report(target_path):
    doc = SimpleDocTemplate(target_path, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18,
                                 textColor=colors.HexColor('#0284c7'), spaceAfter=12)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=12,
                                   textColor=colors.HexColor('#0f172a'), spaceBefore=10, spaceAfter=8)

    story.append(Paragraph("theCFO — Mock Ingestion Documents", title_style))
    story.append(Paragraph("Standard test files synchronized for Manual Mode upload.", styles['Normal']))
    story.append(Spacer(1, 15))

    def build_pdf_table(data_list):
        t = Table(data_list, hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284c7')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        return t

    story.append(Paragraph("1. Invoices & Receivables (invoices_ar.csv)", heading_style))
    story.append(build_pdf_table(ar_data))
    story.append(Spacer(1, 15))

    story.append(Paragraph("2. Financial Statement Ledger (financial_ledger.csv)", heading_style))
    story.append(build_pdf_table(ledger_data))
    story.append(Spacer(1, 15))

    story.append(Paragraph("3. Bank Cash Statement (bank_statement.csv)", heading_style))
    story.append(build_pdf_table(bank_data))

    doc.build(story)
    print(f"✅ PDF saved directly to Downloads: {target_path}")


def render_table_image(data_list, title, target_path):
    df = pd.DataFrame(data_list[1:], columns=data_list[0])
    fig, ax = plt.subplots(figsize=(7, 2.5))
    ax.axis('tight')
    ax.axis('off')

    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.3)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor('#0284c7')
            cell.set_text_props(color='white', weight='bold')
        else:
            cell.set_facecolor('#f8fafc' if row % 2 == 0 else '#ffffff')

    plt.title(title, fontsize=11, weight='bold', pad=10, color='#0f172a')
    plt.savefig(target_path, bbox_inches='tight', dpi=200)
    plt.close()
    print(f"✅ Image saved directly to Downloads: {target_path}")


if __name__ == "__main__":
    # Generate files directly in Downloads folder
    generate_pdf_report(pdf_path)
    render_table_image(ar_data, "Invoices & Receivables (1. Invoices)", ar_img_path)
    render_table_image(ledger_data, "Financial Statement Ledger (2. Ledgers)", ledger_img_path)
    render_table_image(bank_data, "Bank Cash Statement (3. Bank Logs)", bank_img_path)

    # Automatically open File Explorer pointing to Downloads
    os.startfile(DOWNLOADS_DIR)

