import abc
import pathlib
from typing import Iterable
from datetime import datetime

import pandas as pd

TIME_FORMAT = "%Y-%m-%dT%H-%M-%S"

DEFAULT_SAVE_PATH: pathlib.Path = pathlib.Path(
    f"./saved_documents/{datetime.now().strftime(TIME_FORMAT)}.xlsx")
DEFAULT_SAVE_PATH.parent.mkdir(parents=True, exist_ok=False)


class TableWriter(abc.ABC):
    """Table-format writer abstract class"""
    @abc.abstractmethod
    def __init__(self, rows: Iterable[Iterable]) -> None:
        pass

    @abc.abstractmethod
    def set_rows(self, rows: Iterable[Iterable]) -> None:
        """Setter for the inner rows list variable"""

    @abc.abstractmethod
    def write_to_file(self, file_path: str, header_row: Iterable[str]):
        """Writer abstract method"""


class ExcelWriter(TableWriter):
    """Excel implementation for the TableWriter abstract class"""

    def __init__(self, rows: Iterable[Iterable]) -> None:
        super().__init__(rows)
        self.__dataframe: pd.DataFrame = pd.DataFrame(data=rows)

    def set_rows(self, rows: Iterable[Iterable]) -> None:
        self.__dataframe = pd.DataFrame(data=rows)

    def write_to_file(self, file_path: str = DEFAULT_SAVE_PATH,
                            header_row: Iterable[str] = None) -> None:
        self.__dataframe.to_excel(file_path, index=False, header=header_row)
