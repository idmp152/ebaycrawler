import parsing.requesters as requesters
import parsing.parsers as parsers
import fileio.writers as writers
import argparse

from typing import Iterable, Tuple, List

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


def parse_list_pages(urls: Iterable[str], file_path: str = None) -> None:
    requester: requesters.AsynchronousRequester = requesters.AsynchronousRequester(urls)
    parser: parsers.EbayParser = parsers.EbayParser(requester)

    rows: List = []
    header_row: Tuple = ("Item", "Price", "Currency")
    for item in parser.parse_items_from_list_pages():
        rows.append([item.name, item.price, item.currency])

    excel_writer: writers.ExcelWriter = writers.ExcelWriter(rows)
    if file_path is not None:
        excel_writer.write_to_file(file_path, header=header_row)
    else:
        excel_writer.write_to_file(header=header_row)


def main() -> None:
    args_parser: argparse.ArgumentParser = argparse.ArgumentParser()
    actions: Tuple = (
        (("--urls", "-u"), {"dest": "urls", "nargs": '+', "required": True, "help": URLS_ARG_HELP_STRING}),
        (("--mode", "-m"),
         {"dest": "mode", "choices": parsers.MODE_STRINGS, "required": True, "help": MODE_ARG_HELP_STRING}),
        (("--file-path", "-fp"), {"dest": "file_path", "nargs": '?', "help": FILE_PATH_ARG_HELP_STRING})
    )
    for action in actions:
        args_parser.add_argument(*action[0], **action[1])
    args: argparse.Namespace = args_parser.parse_args()

    if parsers.ParsingModes(args.mode) == parsers.ParsingModes.LIST_PAGE:
        parse_list_pages(args.urls, args.file_path)


if __name__ == "__main__":
    main()
