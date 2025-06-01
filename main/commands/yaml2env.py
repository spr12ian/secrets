from main.classes.yaml_helper import YamlHelper
from main.classes.config import Config

def main(args):
    print("🔄 Running yaml2env...")
    if (len(args) > 0):
        print("Arguments:", args)

    config = Config()
    YAML_ENV_FILE = config.YAML_ENV_FILE
    SETENV_FILE = config.SETENV_FILE

    """Load secrets from YAML file into environment variables."""
    env_file = YamlHelper(YAML_ENV_FILE)
    secrets = env_file.read()

    with open(SETENV_FILE, "w") as bash_file:
        bash_file.write(f"#!/bin/bash\n\n")
        for k, v in secrets.items():
            bash_file.write(f"export {k}={v}\n")
    print(
        f"Set {len(secrets)} environment variables by running `source {SETENV_FILE}`."
    )
