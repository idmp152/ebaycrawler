import bs4
from parsing.requesters import Requester
from collections import namedtuple
from typing import List, Iterable
from enum import Enum


class EbayPageParser:
    Item = namedtuple("Item", ["name", "price"])

    def __init__(self, pages: Iterable[str]) -> None:
        self.__soups: List[bs4.BeautifulSoup] = self._get_soups_from_pages(pages)

    def set_pages(self, pages: Iterable[str]) -> None:
        self.__soups = self._get_soups_from_pages(pages)

    def parse_items_from_list_pages(self) -> List[Item]:
        items: List[EbayPageParser.Item] = []
        for soup in self.__soups:
            names = soup.find_all("img", {"class": "s-item__image-img"})
            prices = soup.find_all("span", {"class": "s-item__price"})
            for name, price in zip(names, prices):
                item_name = name["alt"]
                item_price = float(''.join((price.string or price.find("span", {"class": "ITALIC"}).string)
                                           .split(' ')[:-1])
                                   .replace('\xa0', '')
                                   .replace(',', '.'))
                items.append(self.Item(name=item_name, price=item_price))
        return items

    @staticmethod
    def _get_soups_from_pages(pages: Iterable[str]) -> List[bs4.BeautifulSoup]:
        return [bs4.BeautifulSoup(page, "html.parser") for page in pages]


class EbayParser:
    def __init__(self, requester: Requester):
        self.__requester = requester
        self.__page_parser = EbayPageParser(self.__requester.parse_urls())

    def parse_items_from_list_pages(self):
        return self.__page_parser.parse_items_from_list_pages()


class ParsingModes(str, Enum):
    LIST_PAGE = "list"
    # TODO: Do CARD_PAGE parsing


MODE_STRINGS = tuple(ParsingModes)
