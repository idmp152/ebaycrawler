from typing import List, Iterable, NamedTuple, Tuple
from enum import Enum

import bs4

from ebaycrawler.parsing.requesters import Requester #pylint: disable = import-error
from ebaycrawler.logger import logger # pyright: reportMissingImports=false

class Item(NamedTuple):
    """Base Item class"""
    name: str
    price: float
    currency: str


class EbayPageParser:
    """Parses HTML pages into Item objects"""
    def __init__(self, pages: Iterable[str]) -> None:
        self.__soups: Tuple[bs4.BeautifulSoup] = self.__get_soups_from_pages(pages)

    def set_pages(self, pages: Iterable[str]) -> None:
        """Setter for the inner pages list variable"""
        self.__soups = self.__get_soups_from_pages(pages)

    def parse_items_from_list_pages(self) -> Tuple[Item]:
        """Parses every page in the pages list"""
        items: List[Item] = []
        for soup in self.__soups:
            items.extend(self.__parse_single_list_page(soup))
        return tuple(items)

    @staticmethod
    def __parse_single_list_page(soup: bs4.BeautifulSoup) -> Tuple[Item]:
        """Parses a single page"""
        items: List[Item] = []
        names: bs4.element.ResultSet = soup.find_all("img", {"class": "s-item__image-img"})
        prices: bs4.element.ResultSet = soup.find_all("span", {"class": "s-item__price"})
        for name, price in zip(names, prices):
            items.append(EbayPageParser.__parse_single_list_item(name, price))
        return tuple(items)

    @staticmethod
    def __parse_single_list_item(name_element: bs4.PageElement,
                            price_element: bs4.PageElement) -> Item:
        """Parses a single item"""
        price_string = price_element.find_next("span",
                {"class": "ITALIC"}).string.split()[-1].replace(',', '')
        currency = price_string[0]
        price = float(price_string.replace(currency, ''))

        return Item(name=name_element["alt"], price=price, currency=currency)

    @staticmethod
    def __get_soups_from_pages(pages: Iterable[str]) -> Tuple[bs4.BeautifulSoup]:
        return tuple(bs4.BeautifulSoup(page, "html.parser") for page in pages)


class EbayParser:
    """EbayPageParser and Requester mediator class"""
    def __init__(self, requester: Requester):
        self.__requester: Requester = requester
        logger.info("Requesting...")
        self.__page_parser: EbayPageParser = EbayPageParser(self.__requester.parse_urls())

    def parse_items_from_list_pages(self) -> Tuple[Item]:
        """parse_items_from_list_pages from EbayPageParser class"""
        return self.__page_parser.parse_items_from_list_pages()


class ParsingModes(str, Enum):
    """Page parsing mode e.g. list/card"""
    LIST_PAGE: str = "list"
    # TODO: Do CARD_PAGE parsing


MODE_STRINGS = tuple(ParsingModes)
