from fpdf import FPDF
import os
from datetime import datetime

def generate_pdf(sheet):
    data = sheet.get_all_records()[-10:]
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="IZEL Booking — Oxirgi 10 mijoz", ln=True, align='C')
    pdf.ln(10)

    for row in data:
        pdf.cell(200, 10, txt=f"{row.get('client_name')} | {row.get('phone')} | {row.get('route')} | {row.get('status')}", ln=True)

    os.makedirs("reports", exist_ok=True)
    path = f"reports/mijozlar_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    pdf.output(path)
    return path
