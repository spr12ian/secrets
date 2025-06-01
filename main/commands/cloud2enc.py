from main.classes.config import Config
from main.classes.google_drive_helper import GoogleDriveHelper

def main(args):
    print("🔄 Running cloud2enc...")
    if (len(args) > 0):
        print("Arguments:", args)
    # Real logic would go here
    config = Config()
    VAULT_FILE = config.VAULT_FILE

    # Download and decrypt a file from Google Drive
    drive_sync = GoogleDriveHelper()
    drive_sync.download_file("DRIVE_FILE_ID", VAULT_FILE)