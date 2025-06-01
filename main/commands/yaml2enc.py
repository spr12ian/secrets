from main.classes.yaml_helper import YamlHelper
from main.classes.config import Config

def main(args):
    print("🔄 Running yaml2enc...")
    if (len(args) > 0):
        print("Arguments:", args)
        
    config = Config()
    YAML_ENV_FILE = config.YAML_ENV_FILE
    VAULT_FILE = config.VAULT_FILE
    
    env_file = YamlHelper(YAML_ENV_FILE)
    data = env_file.read()

    vault_file = YamlHelper(VAULT_FILE)
    vault_file.write(data)
