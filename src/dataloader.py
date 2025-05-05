import json
import subprocess
from collections.abc import Iterable
from os import PathLike
from typing import AnyStr, Optional

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from .config import BIN_PATH
from .utils import get_absolute_path


class DataLoader:
    """A class to process TSDB blocks and store the data internally.

    This class provides methods to read (multiple) blocks and export the data to various formats.

    Attributes:
        min_ts_millis: If not None, the minimum timestamp (in milliseconds) of samples.
        max_ts_millis: If not None, the maximum timestamp (in milliseconds) of samples.
    """

    def __init__(
        self,
        min_ts_millis: Optional[int] = None,
        max_ts_millis: Optional[int] = None,
        *,
        combine_samples: bool = True,
    ) -> None:
        """Initializes the instance with min and max timestamps, and how to store data.

        Args:
            min_ts_millis: If not None, the minimum timestamp of kept samples.
            max_ts_millis: If not None, the maximum timestamp of kept samples.
            combine_samples: Defines if multiple entries for the same metric should be
                combined into a single entry. If False, multiple entries for the same
                metric will appear as multiple rows.
        """
        self.min_ts_millis = min_ts_millis
        self.max_ts_millis = max_ts_millis
        self.__combine_samples = combine_samples

        self.data = {} if self.__combine_samples else []

    def __len__(self) -> int:
        return len(self.data)

    def read_block(self, path: PathLike[AnyStr] | AnyStr) -> None:
        """Reads a TSDB block at a given path."""
        path = get_absolute_path(path)
        iterator = self._iter_samples(path)

        if self.__combine_samples:
            self._add_to_dict(iterator)
        else:
            self._add_to_list(iterator)

    def to_dataframe(self) -> pd.DataFrame:
        """Returns a pandas dataframe containing the read data."""
        if self.__combine_samples:
            return pd.DataFrame.from_dict(self.data, orient="index")
        else:
            return pd.DataFrame(self.data)

    def to_parquet(self, path: PathLike[AnyStr] | AnyStr) -> None:
        """Exports the read data to Parquet format."""
        path = get_absolute_path(path)
        self.to_dataframe().to_parquet(path)

    def to_tsv(self, path: PathLike[AnyStr] | AnyStr) -> None:
        """Exports the read data to TSV format."""
        path = get_absolute_path(path)
        self.to_dataframe().to_csv(path, sep="\t", index=False)

    def _iter_samples(
        self, path: str
    ) -> Iterable[tuple[str, NDArray[np.float64], NDArray[np.int64]]]:
        """Calls prometheus-tsdb-dump and iterates through the samples."""
        command = [BIN_PATH, "-block", path]

        if self.min_ts_millis:
            command += ["-min-timestamp", str(self.min_ts_millis)]
        if self.max_ts_millis:
            command += ["-max-timestamp", str(self.max_ts_millis)]

        with subprocess.Popen(command, stdout=subprocess.PIPE) as process:
            for line in process.stdout:
                data = json.loads(line.decode().rstrip())

                metric = json.dumps(data["metric"])
                values = np.array(data["values"], dtype=np.float64)
                timestamps = np.array(data["timestamps"], dtype=np.int64)

                yield metric, values, timestamps

    def _add_to_list(self, sample_iterator: Iterable) -> None:
        for metric, values, timestamps in sample_iterator:
            self.data.append(
                {"metric": metric, "values": values, "timestamps": timestamps}
            )

    def _add_to_dict(self, sample_iterator: Iterable) -> None:
        for metric, values, timestamps in sample_iterator:
            if metric not in self.data:
                self.data[metric] = {"values": values, "timestamps": timestamps}
            else:
                self.data[metric]["values"] = np.concatenate(
                    (self.data[metric]["values"], values)
                )
                self.data[metric]["timestamps"] = np.concatenate(
                    (self.data[metric]["timestamps"], timestamps)
                )
