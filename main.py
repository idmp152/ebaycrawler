import parsing.requesters as requesters
import parsing.parsers as parsers
import fileio.writers as writers
import argparse

from typing import Iterable


def parse_list_pages(urls: Iterable[str], file_path: str = None):
    requester = requesters.AsynchronousRequester(urls)
    parser = parsers.EbayParser(requester)

    rows = []
    header_row = ("Item", "Price")
    for item in parser.parse_items_from_list_pages():
        rows.append([item.name, item.price])

    excel_writer = writers.ExcelWriter(rows)
    if file_path is not None:
        excel_writer.write_to_file(file_path, header=header_row)
    else:
        excel_writer.write_to_file(header=header_row)


def main():
    args_parser = argparse.ArgumentParser()
    actions = (
        (("--urls", "-u"), {"dest": "urls", "nargs": '+', "required": True}),
        (("--mode", "-m"), {"dest": "mode", "choices": parsers.MODE_STRINGS, "required": True}),
        (("--file-path", "-fp"), {"dest": "file_path", "nargs": '?'})
    )
    for action in actions:
        args_parser.add_argument(*action[0], **action[1])
    args = args_parser.parse_args()  # TODO: add -h documentation

    if parsers.ParsingModes(args.mode) == parsers.ParsingModes.LIST_PAGE:
        parse_list_pages(args.urls, args.file_path)


if __name__ == "__main__":
    main()
