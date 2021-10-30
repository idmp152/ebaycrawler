import aiohttp
import asyncio
import abc
import requests
from typing import Iterable, List


class Requester(abc.ABC):
    @abc.abstractmethod
    def __init__(self, urls: Iterable[str]):
        pass

    @abc.abstractmethod
    def parse_urls(self) -> Iterable[str]:
        pass

    @abc.abstractmethod
    def _parse_single(self, url) -> str:
        pass

    @abc.abstractmethod
    def set_urls(self, urls: Iterable[str]):
        pass


class SynchronousRequester(Requester):
    def __init__(self, urls: Iterable[str]):
        super().__init__(urls)
        self.__urls: Iterable[str] = urls

    def set_urls(self, urls: Iterable[str]):
        self.__urls = urls

    def parse_urls(self) -> List[str]:
        return [self._parse_single(url) for url in self.__urls]

    def _parse_single(self, url) -> str:
        return requests.get(url).content


class AsynchronousRequester(Requester):
    def __init__(self, urls: Iterable[str]):
        super().__init__(urls)
        self.__urls = urls
        self.__event_loop = asyncio.get_event_loop()
        self.__session = None

    def set_urls(self, urls: Iterable[str]):
        self.__urls = urls

    def parse_urls(self) -> List[str]:
        return self.__event_loop.run_until_complete(self._parse_urls_async())

    async def _parse_urls_async(self) -> List[str]:
        self.__session = aiohttp.ClientSession()
        async with self.__session:
            tasks = []
            for url in self.__urls:
                task = asyncio.create_task(self._parse_single(url))
                tasks.append(task)
            return await asyncio.gather(*tasks)

    async def _parse_single(self, url) -> str:
        async with self.__session.get(url) as response:
            return await response.text()
