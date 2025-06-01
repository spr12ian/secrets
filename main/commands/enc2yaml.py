from main.classes.yaml_helper import YamlHelper
from main.classes.config import Config


def main(args):
    print("🔄 Running enc2yaml...")
    if (len(args) > 0):
        print("Arguments:", args)

    config = Config()
    VAULT_FILE = config.VAULT_FILE
    YAML_DECRYPTED_FILE = config.YAML_DECRYPTED_FILE

    vault_file = YamlHelper(VAULT_FILE)
    data = vault_file.read()

    decrypted_file = YamlHelper(YAML_DECRYPTED_FILE)
    decrypted_file.write(data)
