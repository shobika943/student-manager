"""Persistence layer: reads/writes students to a JSON file."""
import json
import os
import tempfile
from typing import List

from .models import Student


class StorageError(Exception):
    """Raised when the data file cannot be read or written."""


class JsonRepository:
    def __init__(self, path: str = "data/students.json"):
        self.path = path

    def load_all(self) -> List[Student]:
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return [Student.from_dict(d) for d in json.loads(content)]
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise StorageError(
                f"Data file '{self.path}' is corrupt ({exc}). "
                "Fix or delete it to continue."
            ) from exc
        except OSError as exc:
            raise StorageError(f"Cannot read '{self.path}': {exc}") from exc

    def save_all(self, students: List[Student]) -> None:
        """Write atomically so a crash never leaves a half-written file."""
        directory = os.path.dirname(os.path.abspath(self.path))
        try:
            os.makedirs(directory, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=directory, suffix=".tmp")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump([s.to_dict() for s in students], f, indent=2)
            os.replace(tmp, self.path)
        except OSError as exc:
            raise StorageError(f"Cannot write '{self.path}': {exc}") from exc
