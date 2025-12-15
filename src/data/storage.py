from pathlib import Path
from typing import Any, Union

from ruamel.yaml import YAML, YAMLError


class YAMLStorage:
    """
    Handles YAML file operations with comment preservation and YAML 1.2 support.
    """

    def __init__(self) -> None:
        self._yaml = YAML()
        self._yaml.preserve_quotes = True
        self._yaml.indent(mapping=2, sequence=4, offset=2)

    def load(self, file_path: Union[str, Path]) -> Any:
        """
        Load data from a YAML file.

        Args:
            file_path: Path to the YAML file.

        Returns:
            The parsed data structure.

        Raises:
            YAMLError: If parsing fails.
            FileNotFoundError: If the file does not exist.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            try:
                return self._yaml.load(f)
            except YAMLError as e:
                raise YAMLError(f"Failed to parse YAML file {path}: {e}") from e

    def save(self, data: Any, file_path: Union[str, Path]) -> None:
        """
        Save data to a YAML file, preserving structure and comments.

        Args:
            data: The data structure to save.
            file_path: Path where the file should be saved.
        """
        path = Path(file_path)
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            self._yaml.dump(data, f)
