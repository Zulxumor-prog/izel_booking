from fpdf import FPDF
import os
from datetime import datetime

def generate_chek(data):
    os.makedirs("reports", exist_ok=True)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="IZEL Booking — Mijoz Check", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Ism: {data.get('client_name', '')}", ln=True)
    pdf.cell(200, 10, txt=f"Telefon: {data.get('phone', '')}", ln=True)
    pdf.cell(200, 10, txt=f"Yo‘nalish: {data.get('route', '')}", ln=True)
    pdf.cell(200, 10, txt=f"Tracking ID: {data.get('tracking_id', '')}", ln=True)
    pdf.cell(200, 10, txt=f"Sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)

    # QR-kod rasmi (agar mavjud bo‘lsa)
    qr_path = data.get("qr_path")
    if qr_path and os.path.exists(qr_path):
        pdf.image(qr_path, x=70, y=100, w=60)

    file_path = f"reports/{data.get('tracking_id', 'noid')}_chek.pdf"
    pdf.output(file_path)
    return file_path
