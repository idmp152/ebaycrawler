import asyncio
import abc
from typing import Iterable, Tuple, List

import aiohttp
import requests

class Requester(abc.ABC):
    """Requester abstract class"""
    @abc.abstractmethod
    def __init__(self, urls: Iterable[str]) -> None:
        pass

    @abc.abstractmethod
    def parse_urls(self) -> Iterable[str]:
        """Requests given urls and returns the responses"""

    @abc.abstractmethod
    def _parse_single(self, url) -> str:
        pass

    @abc.abstractmethod
    def set_urls(self, urls: Iterable[str]) -> None:
        """Setter for the inner urls list variable"""


class SynchronousRequester(Requester):
    """Synchronous implementation for the Requester abstract class"""
    def __init__(self, urls: Iterable[str]) -> None:
        super().__init__(urls)
        self.__urls: Iterable[str] = urls

    def set_urls(self, urls: Iterable[str]) -> None:
        self.__urls = urls

    def parse_urls(self) -> Tuple[str]:
        return tuple(self._parse_single(url) for url in self.__urls)

    def _parse_single(self, url) -> str:
        return requests.get(url).text


class AsynchronousRequester(Requester):
    """Asynchronous implementation for the Requester abstract class"""
    def __init__(self, urls: Iterable[str]) -> None:
        super().__init__(urls)
        self.__urls: Iterable[str] = urls
        self.__event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.__session = None

    def set_urls(self, urls: Iterable[str]) -> None:
        self.__urls = urls

    def parse_urls(self) -> Tuple[str]:
        return self.__event_loop.run_until_complete(self._parse_urls_async())

    async def _parse_urls_async(self) -> Tuple:
        self.__session = aiohttp.ClientSession()
        async with self.__session:
            tasks: List[asyncio.Task] = []
            for url in self.__urls:
                task: asyncio.Task = asyncio.create_task(self._parse_single(url))
                tasks.append(task)
            return await asyncio.gather(*tasks)

    async def _parse_single(self, url) -> str: #pylint: disable = invalid-overridden-method
        async with self.__session.get(url) as response:
            return await response.text()
