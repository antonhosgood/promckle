import os
from typing import Union


def get_absolute_path(path: Union[str, bytes, os.PathLike]) -> str:
    """Return an absolute path with expanded ~ constructions."""
    return os.path.abspath(os.path.expanduser(path))
