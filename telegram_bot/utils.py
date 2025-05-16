import os
from datetime import datetime
import qrcode

# 1. Har bir mijoz uchun noyob tracking ID
def generate_tracking_id():
    return "IZ-" + datetime.now().strftime("%Y%m%d-%H%M%S")

# 2. Faylni media/ papkaga saqlash
def save_file(folder, filename, content):
    path = f"media/{folder}/"
    os.makedirs(path, exist_ok=True)
    full_path = os.path.join(path, filename)
    with open(full_path, 'wb') as f:
        f.write(content)
    return full_path

# 3. QR-kod yaratish
def generate_qr(data):
    path = f"media/qr/{data}.png"
    os.makedirs("media/qr", exist_ok=True)
    img = qrcode.make(data)
    img.save(path)
    return path
