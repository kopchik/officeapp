#!/usr/bin/env python3

import asyncio
from typing import List, Union

from fastapi import FastAPI, HTTPException, Query, Response
from pydantic import BaseModel

from integrations import GiteaSearch, GithubSearch
from schemas import SearchResults

app = FastAPI(
    title="Repo Octosearch", description="A code for an interview.", version="1.0.0"
)
search_engines = {"gitea": GiteaSearch(), "github": GithubSearch()}


class ValidationError(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=400, detail=detail)


class SearchResponse(BaseModel):
    repos: SearchResults
    errors: List[str]


@app.get("/search-repos", response_model=SearchResponse)
async def search(
    response: Response,
    q: str = Query(
        None,
        min_length=2,
        max_length=50,
        regex="^[a-zA-A0-9_]+$",
        description="query string",
    ),
    engines: str = Query(
        "gitea", description="comma-separated list of engines, e.g. `gitea,github`"
    ),
):
    """Search for a repository using one or more search engines."""

    engines_ = _parse_engines(engines)
    awaitables = [engine.search(q) for engine in engines_]
    results = await asyncio.gather(*awaitables, return_exceptions=True)
    repos, errors = _merge_search_results(results)
    return SearchResponse(repos=repos, errors=errors)


def _parse_engines(s):
    engines = []
    for engine_name in s.split(","):
        if engine_name not in search_engines:
            raise ValidationError(f"unknown engine {engine_name}")
        engines.append(search_engines[engine_name])
    return engines


def _merge_search_results(results: List[Union[SearchResults, Exception]]):
    """Merge results from multiple integrations"""
    errors = []
    repos = []
    for r in results:
        if isinstance(r, Exception):
            errors.append(str(r))
            continue
        repos.extend(r)
    repos.sort(key=lambda e: e.name.lower())
    return SearchResults(__root__=repos), errors


class AvailableEnginesResponse(BaseModel):
    __root__: List[str]


@app.get("/available-engines", response_model=AvailableEnginesResponse)
async def available_engines():
    """Get available search engines."""
    return AvailableEnginesResponse(__root__=sorted(search_engines.keys()))
