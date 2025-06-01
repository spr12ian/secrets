from main.classes.yaml_helper import YamlHelper
from main.classes.config import Config
import os


def main(args):
    print("🔄 Running env2yaml...")
    if (len(args) > 0):
        print("Arguments:", args)
    # Real logic would go here
    config = Config()
    YAML_ENV_FILE = config.YAML_ENV_FILE
    env_file = YamlHelper(YAML_ENV_FILE)
    env_file.write(dict(os.environ))
