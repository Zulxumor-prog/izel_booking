from fpdf import FPDF
import os
from datetime import datetime

def generate_pdf(sheet):
    rows = sheet.get_all_records()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="IZEL Mijozlar Ro'yxati", ln=True, align='C')
    pdf.ln(10)

    for row in rows[-10:]:
        pdf.cell(200, 10, txt=f"{row['client_name']} — {row['route']} — {row['status']}", ln=True)

    pdf_path = f"reports/clients_{datetime.now().date()}.pdf"
    os.makedirs("reports", exist_ok=True)
    pdf.output(pdf_path)
    return pdf_path
