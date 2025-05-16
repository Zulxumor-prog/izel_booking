from drive_uploader import upload_file
from sheet_writer import write_to_sheet

# Fayl yo'llari (telefon orqali kelgan fayllar joylashgan bo‘lishi kerak)
passport_path = 'downloads/passports/hargos.png'
photo_path = 'downloads/photos/3x4.jpg'
check_path = 'downloads/checks/receipt.jpg'

# 1. Fayllarni Drive’ga yuklaymiz
passport_url = upload_file(passport_path)
photo_url = upload_file(photo_path)
check_url = upload_file(check_path)

# 2. Sheets faylga yozamiz
write_to_sheet(
    agent="Zulxumor",
    client_name="Asal",
    phone="+998901234567",
    direction="Yiwu",
    date="2025-05-07",
    passport_link=passport_url,
    photo_link=photo_url,
    check_link=check_url
)
