import sys
import importlib

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m main <command>")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    try:
        module = importlib.import_module(f"main.commands.{command}")
    except ImportError:
        print(f"Unknown command: {command}")
        sys.exit(1)

    if not hasattr(module, "main"):
        print(f"Command '{command}' does not have a main() function.")
        sys.exit(1)

    module.main(args)

if __name__ == "__main__":
    main()
