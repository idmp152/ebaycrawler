import abc
from typing import Iterable, Type

import pandas as pd

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

    def write_to_file(self, file_path: str, header_row: Iterable[str] = None) -> str:
        self.__dataframe.to_excel(file_path, index=False, header=header_row)
        return file_path

class CsvWriter(TableWriter):
    """CSV implementation for the TableWriter abstract class"""

    def __init__(self, rows: Iterable[Iterable]) -> None:
        super().__init__(rows)
        self.__dataframe: pd.DataFrame = pd.DataFrame(data=rows)

    def set_rows(self, rows: Iterable[Iterable]) -> None:
        self.__dataframe = pd.DataFrame(data=rows)

    def write_to_file(self, file_path: str, header_row: Iterable[str] = None) -> str:
        self.__dataframe.to_csv(file_path, index=False, header=header_row)
        return file_path

def get_writer_by_extension(file_extension: str) -> Type[TableWriter] | None:
    """Gets WriterType by file extension"""
    if file_extension == "csv":
        return CsvWriter
    if file_extension == "xlsx":
        return ExcelWriter
    return None
