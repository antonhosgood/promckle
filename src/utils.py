import os
from os import PathLike
from typing import AnyStr


def get_absolute_path(path: PathLike[AnyStr] | AnyStr) -> AnyStr:
    """Return the absolute path, expanding any '~' to the user's home directory."""
    return os.path.abspath(os.path.expanduser(path))
