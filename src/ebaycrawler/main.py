import argparse
from typing import Iterable, Tuple, List, NamedTuple

from colorama import Fore, Style

#pylint: disable = import-error
from ebaycrawler.parsing import requesters
from ebaycrawler.parsing import parsers
from ebaycrawler.fileio import writers
from ebaycrawler.logger import logger
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

R = Fore.RED
B = Fore.BLUE
Y = Fore.YELLOW
G = Fore.GREEN
E = Style.RESET_ALL

TEXT_LOGO: str = (
    rf"""
{R}       _          {E}{B}            {E}{Y}                  {E}{G} _{E}
{R}      | |         {E}{B}            {E}{Y}                  {E}{G}| |{E}
{R}   ___| |__   __ _{E}{B} _   _  ___ {E}{Y}_ __ __ ___      _{E}{G}| | ___ _ __{E}
{R}  / _ \ '_ \ / _` {E}{B}| | | |/ __|{E}{Y} '__/ _` \ \ /\ / {E}{G}/ |/ _ \ '__|{E}
{R} |  __/ |_) | (_| {E}{B}| |_| | (__|{E}{Y} | | (_| |\ V  V /{E}{G}| |  __/ |{E}
{R}  \___|_.__/ \__,_{E}{B}|\__, |\___|{E}{Y}_|  \__,_| \_/\_/ {E}{G}|_|\___|_|{E}
{R}                  {E}{B}  __/ |     {E}{Y}                  {E}
{R}                  {E}{B} |___/      {E}{Y}                  {E}
    """
)

TEXT_DELIMITER = '-' * max(len(i) for i in TEXT_LOGO.split('\n'))

class Argument(NamedTuple):
    """Argument object for the argparse library."""
    dest: str = None
    nargs: str = None
    required: bool = None
    help: str = None
    choices: tuple = None


def parse_list_pages(urls: Iterable[str], file_path: str = None) -> str:
    """Ready to use list pages parsing function."""
    requester: requesters.AsynchronousRequester = requesters.AsynchronousRequester(urls)
    parser: parsers.EbayParser = parsers.EbayParser(requester)

    rows: List = []
    header_row: Tuple = ("Item", "Price", "Currency")
    for item in parser.parse_items_from_list_pages():
        rows.append([item.name, item.price, item.currency])

    excel_writer: writers.ExcelWriter = writers.ExcelWriter(rows)
    if file_path is not None:
        return excel_writer.write_to_file(file_path, header_row=header_row)
    return excel_writer.write_to_file(header_row=header_row)


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
    logger.info("Parsing...")
    if parsers.ParsingModes(args.mode) == parsers.ParsingModes.LIST_PAGE:
        saved_path = parse_list_pages(args.urls, args.file_path)
    logger.success("Parsing completed!")
    logger.info("Saved to -> %s", saved_path)

if __name__ == "__main__":
    main()
