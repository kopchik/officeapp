import logging
import os
from abc import ABC, abstractmethod

import aiohttp
import ujson

from schemas import SearchResult, SearchResults


class IntegrationError(Exception):
    pass


class Search(ABC):
    @abstractmethod
    async def search(self, query: str) -> [SearchResult]:
        ...


class GithubSearch(Search):
    """TODO: search only in master branch, only in repository name"""

    def __init__(self, timeout=None):
        self.timeout = timeout
        headers = {"Accept": "application/vnd.github.v3+json"}
        # TODO: shutdown session at exit?
        self.session = aiohttp.ClientSession(
            headers=headers, json_serialize=ujson.dumps
        )

    # TODO: security: sanitize search query
    # TODO: error handling
    async def search(self, query: str) -> [SearchResult]:
        url = "https://api.github.com/search/repositories"
        params = {"q": f"{query} in:name"}
        async with self.session.get(
            url, params=params, timeout=self.timeout
        ) as response:
            if response.status != 200:
                self.log.error(response)
                raise IntegrationError(
                    f"unexpected response {response.status} from github"
                )
            # TODO: limit response size
            raw_result = await response.json(loads=ujson.loads)
            processed_result = []
            for item in raw_result["items"]:
                processed_result.append(
                    SearchResult(
                        name=item.get("full_name", ""),
                        size=item.get("size", 0),
                        url=item.get("html_url"),
                        owner=item.get("owner", "").get("login", ""),
                    )
                )
            return processed_result


class GiteaSearch(Search):
    def __init__(self, timeout=10):
        self.initialized = False
        self.log = logging.getLogger("integrations.gitea")
        self.timeout = timeout

        token = os.environ.get("GITEA_TOKEN")
        if not token:
            self.log.critical("no GITEA_TOKEN provided")
            return
        headers = {"Authorization": f"token {token}"}

        url = os.environ.get("GITEA_URL")
        if not url:
            self.log.critical("no GITEA_URL provided")
            return
        # TODO: validate url
        self.url = url

        self.session = aiohttp.ClientSession(
            headers=headers, json_serialize=ujson.dumps
        )

        self.initialized = True

    async def search(self, query: str) -> [SearchResult]:
        if not self.initialized:
            raise IntegrationError(
                "Gitea search not initialized. Did you provide GITEA_TOKEN env var?"
            )
        # TODO: security: sanitize search query
        params = {"q": query}
        async with self.session.get(
            self.url, params=params, timeout=self.timeout
        ) as response:
            if response.status != 200:
                self.log.error(response)
                raise IntegrationError(
                    f"unexpected response status {response.status} from gitea"
                )
            # TODO: limit response size
            raw_result = await response.json(loads=ujson.loads)
            processed_result = []
            for item in raw_result["data"]:
                processed_result.append(
                    # it turned out gitea mimics github api,
                    # so this code looks the same as above :/
                    SearchResult(
                        name=item.get("full_name", ""),
                        size=item.get("size", 0),
                        url=item.get("html_url"),
                        owner=item.get("owner", "").get("login", ""),
                    )
                )
            return SearchResults(__root__=processed_result)
