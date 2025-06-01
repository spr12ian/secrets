from main.classes.config import Config
from main.classes.google_drive_helper import GoogleDriveHelper
from time import strftime


def main(args):
    print("🔄 Running cloud2enc...")
    if len(args) > 0:
        print("Arguments:", args)
        
    config = Config()
    VAULT_FILE = config.VAULT_FILE

    timestamp = strftime("%Y-%m-%d_%H:%M:%S")
    source = VAULT_FILE
    target = f"{timestamp}_{source.name}"

    # Upload to Google Drive
    drive_sync = GoogleDriveHelper()
    drive_sync.upload_file(source, target)
