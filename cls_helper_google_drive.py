import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

class GoogleDriveHelper:
    def __init__(
        self,
        credentials_path: Path = Path("credentials.json"),
        token_path: Path = Path("token.json"),
    ):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = self._authenticate()

    def _load_credentials_from_env(self):
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        if not client_id or not client_secret:
            raise RuntimeError("GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set.")

        return {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"],
            }
        }

    def _authenticate(self):
        creds = None

        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)

        if not creds or not creds.valid:
            if self.credentials_path.exists():
                client_config = str(self.credentials_path)
            else:
                print("credentials.json not found, using environment variables.")
                client_config = self._load_credentials_from_env()

            flow = InstalledAppFlow.from_client_config(client_config, SCOPES) \
                if isinstance(client_config, dict) \
                else InstalledAppFlow.from_client_secrets_file(client_config, SCOPES)

            creds = flow.run_console()

            with open(self.token_path, "w") as token_file:
                token_file.write(creds.to_json())

        return build("drive", "v3", credentials=creds)

    def upload_file(
        self,
        local_path: Path,
        drive_filename: str,
        mime_type="application/octet-stream",
    ):
        media = MediaFileUpload(str(local_path), mimetype=mime_type, resumable=True)
        metadata = {"name": drive_filename}
        file = (
            self.service.files()
            .create(body=metadata, media_body=media, fields="id")
            .execute()
        )
        print(f"Uploaded: {drive_filename} → ID: {file.get('id')}")

    def download_file(self, file_id: str, destination: Path):
        request = self.service.files().get_media(fileId=file_id)
        with open(destination, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%")
