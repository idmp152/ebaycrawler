import bs4
from parsing.requesters import Requester
from collections import namedtuple
from typing import List
from enum import Enum, auto


class EbayParser:
    Item = namedtuple("Item", ["name", "price"])

    def __init__(self, requester: Requester) -> None:
        super().__init__(requester)
        self.__requester: Requester = requester
        self.__soups: List[bs4.BeautifulSoup] = self._get_soups()

    def set_requester(self, requester: Requester) -> None:
        self.__requester = requester
        self.__soups = self._get_soups()

    def parse_items_from_list_pages(self) -> List[Item]:
        items: List[EbayParser.Item] = []
        for soup in self.__soups:
            names = soup.find_all("img", {"class": "s-item__image-img"})
            prices = soup.find_all("span", {"class": "s-item__price"})  # TODO: Fix price ranges pasrsing e.g. 12-15$
            names_iter = iter(names)
            prices_iter = iter(prices)
            for _ in names:
                item_name = next(names_iter)["alt"]
                item_price = float(''.join(next(prices_iter)
                                           .string.split(' ')[:-1])
                                   .replace('\xa0', '')
                                   .replace(',', '.'))
                items.append(self.Item(name=item_name, price=item_price))
        return items

    def _get_soups(self) -> List[bs4.BeautifulSoup]:
        return [bs4.BeautifulSoup(html, "html.parser") for html in self.__requester.parse_urls()]


class ParsingModes(Enum):
    LIST_PAGE = auto()
    # TODO: Do CARD_PAGE parsing
    UNKNOWN = auto()

    @staticmethod
    def get_mode_by_string(string: str):
        string = string.lower()
        if string == "list":
            return ParsingModes.LIST_PAGE
        # elif string == "card":
        #     return ParsingModes.CARD_PAGE
        else:
            return ParsingModes.UNKNOWN
