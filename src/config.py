import os

__all__ = ["BIN_PATH"]

BIN_DIR = os.path.abspath("./promckle/bin")
BIN_NAME = "prometheus-tsdb-dump"

# prometheus-tsdb-dump installation path
BIN_PATH = os.path.join(BIN_DIR, BIN_NAME)
