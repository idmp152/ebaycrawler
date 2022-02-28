import bs4
from parsing.requesters import Requester
from typing import List, Iterable, NamedTuple, Tuple
from enum import Enum


class Item(NamedTuple):
    name: str
    price: float
    currency: str


class EbayPageParser:
    def __init__(self, pages: Iterable[str]) -> None:
        self.__soups: Tuple[bs4.BeautifulSoup] = self._get_soups_from_pages(pages)

    def set_pages(self, pages: Iterable[str]) -> None:
        self.__soups = self._get_soups_from_pages(pages)

    def parse_items_from_list_pages(self) -> Tuple[Item]:
        items: List[Item] = []
        for soup in self.__soups:
            names: bs4.element.ResultSet = soup.find_all("img", {"class": "s-item__image-img"})
            prices: bs4.element.ResultSet = soup.find_all("span", {"class": "s-item__price"})
            for name, price in zip(names, prices):
                item_name = name["alt"]
                raw_price_and_currency: List[str] = (price.string or price.find("span", {"class": "ITALIC"}).string)\
                    .split(' ')
                currency: str = raw_price_and_currency[-1]
                item_price = float(''.join(raw_price_and_currency[:-1])
                                   .replace('\xa0', '')
                                   .replace(',', '.'))
                items.append(Item(name=item_name, price=item_price, currency=currency))
        return tuple(items)

    @staticmethod
    def _get_soups_from_pages(pages: Iterable[str]) -> Tuple[bs4.BeautifulSoup]:
        return tuple(bs4.BeautifulSoup(page, "html.parser") for page in pages)


class EbayParser:
    def __init__(self, requester: Requester):
        self.__requester: Requester = requester
        self.__page_parser: EbayPageParser = EbayPageParser(self.__requester.parse_urls())

    def parse_items_from_list_pages(self) -> Tuple[Item]:
        return self.__page_parser.parse_items_from_list_pages()


class ParsingModes(str, Enum):
    LIST_PAGE: str = "list"
    # TODO: Do CARD_PAGE parsing


MODE_STRINGS = tuple(ParsingModes)
