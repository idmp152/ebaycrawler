import argparse
from typing import Iterable, Tuple, List, NamedTuple, Callable, Any, Type
from datetime import datetime
import pathlib

#pylint: disable = import-error
from ebaycrawler.parsing import requesters, parsers
from ebaycrawler.fileio import writers
from ebaycrawler.logger import logger
from ebaycrawler import exceptions
from ebaycrawler.__init__ import __version__, __author__, __author_email__ #pylint: disable = no-name-in-module
#pylint: enable = import-error

URLS_ARG_HELP_STRING: str = (
    """
    A required argument that represents the urls that have to be parsed e.g.
    --urls https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117 https://www.ebay.com/b/adidas/bn_21818843
    """
)
MODE_ARG_HELP_STRING: str = (
    """
    A required argument that represents the mode in which the provided urls should be parsed e.g.
    --mode=list or -m=card
    """
)
FILE_PATH_ARG_HELP_STRING: str = (
    """
    An optional argument that represents the path where the table with parsed items should be saved
    (./saved_documents/<current_datetime> by default) e.g.
    --file-path=./my_folder/test.xlsx
    """
)

LOGO_PATH = pathlib.Path(__file__).parent /  "./logo.ansi"
TEXT_LOGO: str
with open(LOGO_PATH, "r", encoding="utf-8") as logo_file:
    TEXT_LOGO = logo_file.read()

COLOR_SEGMENTS_LENGTH = 24
TEXT_DELIMITER = '-' * (max(len(line) for line in TEXT_LOGO.split('\n')) - COLOR_SEGMENTS_LENGTH)

class Argument(NamedTuple):
    """Argument object for the argparse library."""
    dest: str = None
    nargs: str = None
    required: bool = None
    help: str = None
    choices: tuple = None


TIME_FORMAT = "%Y-%m-%dT%H-%M-%S"

DEFAULT_SAVE_PATH: pathlib.Path = pathlib.Path(
    f"./saved_documents/{datetime.now().strftime(TIME_FORMAT)}.csv")
DEFAULT_SAVE_PATH.parent.mkdir(parents=True, exist_ok=True)

def parse_list_pages(urls: Iterable[str], file_path: str) -> str:
    """Ready to use list pages parsing function."""
    if file_path is None:
        file_path = str(DEFAULT_SAVE_PATH)

    requester: requesters.AsynchronousRequester = requesters.AsynchronousRequester(urls)
    parser: parsers.EbayParser = parsers.EbayParser(requester)

    rows: List = []
    header_row: Tuple = ("Item", "Price", "Currency")
    for item in parser.parse_items_from_list_pages():
        rows.append([item.name, item.price, item.currency])

    file_format = file_path.split('.')[-1]
    writer_type: Type[writers.TableWriter] = writers.get_writer_by_extension(file_format)

    if writer_type is None:
        raise exceptions.UnknownFileFormatException(file_format)
    writer: writers.TableWriter = writer_type(rows)

    return writer.write_to_file(file_path ,header_row=header_row)

def get_method_by_mode(mode: str) -> Callable | None:
    """Gets parsing method by mode string"""
    if parsers.ParsingModes(mode) == parsers.ParsingModes.LIST_PAGE:
        return parse_list_pages
    return None

def handle_exceptions(func: Callable, *args, **kwargs) -> Any:
    """Handles occuring exceptions"""
    try:
        logger.info("Parsing...")
        return_value = func(*args, **kwargs)
        logger.success("Parsing completed!")
        return return_value
    except exceptions.UnknownFileFormatException as error:
        logger.error("Error! Unknown file format: .%s", error.file_format)
    except BaseException as error: #pylint: disable = broad-except
        logger.error('Error! Unexpected exceptions caught:')
        logger.debug(str(error))
    return None

def main() -> None:
    """Main function"""
    args_parser: argparse.ArgumentParser = argparse.ArgumentParser()
    actions: dict = {
        ("--urls", "-u"):
        Argument(dest="urls", nargs='+', required=True, help=URLS_ARG_HELP_STRING),

        ("--mode", "-m"):
        Argument(dest="mode", choices=parsers.MODE_STRINGS,
                        required=True, help=MODE_ARG_HELP_STRING),

        ("--file-path", "-fp"):
         Argument(dest="file_path", nargs='?', help=FILE_PATH_ARG_HELP_STRING)
    }
    for flags, argument in actions.items():
        args_parser.add_argument(*flags, **argument._asdict())
    args: argparse.Namespace = args_parser.parse_args()

    print(TEXT_LOGO, end='\n\n')
    print(f"Author: {__author__} <{__author_email__}>  Version: {__version__}")
    print(TEXT_DELIMITER)
    path = handle_exceptions(get_method_by_mode(args.mode), args.urls, args.file_path)
    logger.info("Saved to -> %s", path)

if __name__ == "__main__":
    main()
