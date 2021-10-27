import pandas as pd
import abc
from typing import Iterable
from datetime import datetime


class TableWriter(abc.ABC):
    @abc.abstractmethod
    def __init__(self, rows: Iterable[Iterable]):
        pass

    @abc.abstractmethod
    def set_rows(self, rows: Iterable[Iterable]):
        pass

    @abc.abstractmethod
    def write_to_file(self, file_path: str, header_row: Iterable[str]):
        pass


class ExcelWriter(TableWriter):
    __default_file_path = f"./saved_documents/{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.xlsx"

    def __init__(self, rows: Iterable[Iterable]):
        super().__init__(rows)
        self.__rows: Iterable[Iterable] = rows
        self.__dataframe: pd.DataFrame = pd.DataFrame(data=rows)

    def set_rows(self, rows: Iterable[Iterable]):
        self.__rows = rows
        self.__dataframe = pd.DataFrame(data=rows)

    def write_to_file(self, file_path: str = __default_file_path, header: Iterable[str] = None):
        self.__dataframe.to_excel(file_path, index=False, header=header)
