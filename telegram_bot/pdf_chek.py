from fpdf import FPDF
import os
from datetime import datetime

def generate_chek(data, file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Sarlavha
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Booking Chek", ln=True, align='C')
    pdf.ln(10)

    # Ma'lumotlar
    pdf.set_font("Arial", size=12)
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    # Sana va vaqt
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Yaratilgan sana: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)

    # Saqlash
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    pdf.output(file_path)
