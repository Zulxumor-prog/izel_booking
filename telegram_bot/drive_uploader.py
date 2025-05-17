import os
import json 
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.conf import settings

# JSON credentialni atrof-muhit (environment variable) dan o‘qish
credentials_json = os.environ.get("GOOGLE_CREDENTIALS")
credentials_info = json.loads(credentials_json)

# Google API credential yaratish
credentials = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=['https://www.googleapis.com/auth/drive.file']
)

# Drive service yaratish
drive_service = build("drive", "v3", credentials=credentials)

# Yuklovchi funksiya
def upload_file(file_path, file_name, folder_id):
    file_metadata = {
        "name": file_name,
        "parents": [folder_id]
    }
    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()
    return f"https://drive.google.com/file/d/{file.get('id')}/view?usp=sharing"