import os
from pathlib import Path
import re
from typing import Any
import yaml


class ConfigNode:
    def __init__(self, data, path=None, root=None):
        self._data = data or {}
        self._path = path or []
        self._root = root or self

        for key, value in self._data.items():
            if isinstance(value, dict):
                # Recursively nest sub-configs
                setattr(
                    self, key, ConfigNode(value, self._path + [key], root=self._root)
                )
            else:
                # Set terminal values with substitution and env override
                setattr(self, key, self._get_value_with_override(key, value))

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def _get_value_with_override(self, key, original_value):
        env_key = "_".join((self._path + [key])).upper()
        env_value = os.getenv(env_key)
        value = env_value if env_value is not None else original_value
        value = self._substitute_variables(value)
        return self._cast_type(value, original_value)

    def _substitute_variables(self, value):
        if not isinstance(value, str):
            return value

        def replacer(match):
            var = match.group(1)
            # Try environment variable first
            if var in os.environ:
                return os.environ[var]
            # Then try config-defined variable
            try:
                result = self._root.get(var)
                return str(result)
            except Exception:
                return match.group(0)  # Leave as-is if no match

        return re.sub(r"\$\{([^}]+)\}", replacer, value)

    def _cast_type(self, value, original_value):
        if original_value is None:
            return self._maybe_path(value)

        if isinstance(original_value, bool):
            return str(value).lower() in ("1", "true", "yes", "on")
        if isinstance(original_value, int):
            return int(value)
        if isinstance(original_value, float):
            return float(value)

        return self._maybe_path(value)

    def _maybe_path(self, value):
        if isinstance(value, str):
            expanded = os.path.expanduser(value)
            expanded = os.path.expandvars(expanded)
            p = Path(expanded)
            if "/" in value or "\\" in value or p.exists() or p.parent.exists():
                return p
        return value

    def get(self, dotted_key, default=None):
        keys = dotted_key.split(".")
        node = self
        path = []
        for key in keys:
            path.append(key)
            if hasattr(node, key):
                node = getattr(node, key)
            else:
                # Attempt environment fallback
                env_key = "_".join(path).upper()
                env_value = os.getenv(env_key)
                if env_value is not None:
                    return env_value
                return default
        return node


class Config(ConfigNode):
    def __init__(self, yaml_path="config.yaml"):
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
        super().__init__(data)

        # Create VAULT_DIR if it is a Path and doesn't exist
        vault_dir = getattr(self, "VAULT_DIR", None)
        if isinstance(vault_dir, Path) and not vault_dir.exists():
            vault_dir.mkdir(parents=True, exist_ok=True)

