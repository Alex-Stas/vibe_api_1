"""Thin HTTP helpers on top of requests: GET/POST, timeouts, status checks."""

from __future__ import annotations

from typing import Any, Mapping

import requests

DEFAULT_TIMEOUT = 10


def get(
    url: str,
    params: Mapping[str, Any] | None = None,
    timeout: float | int = DEFAULT_TIMEOUT,
    **kwargs: Any,
) -> requests.Response:
    """GET-запрос. Сетевые ошибки — ``requests.RequestException``."""
    return requests.get(url, params=params, timeout=timeout, **kwargs)


def post(
    url: str,
    *,
    json: Any = None,
    data: Any = None,
    params: Mapping[str, Any] | None = None,
    timeout: float | int = DEFAULT_TIMEOUT,
    **kwargs: Any,
) -> requests.Response:
    """POST-запрос. Сетевые ошибки — ``requests.RequestException``."""
    return requests.post(
        url, json=json, data=data, params=params, timeout=timeout, **kwargs
    )


def ok(response: requests.Response) -> bool:
    """True, если статус 2xx (как ``response.ok``)."""
    return response.ok


def raise_unless_ok(response: requests.Response) -> None:
    """Бросает ``requests.HTTPError``, если статус не успешный."""
    response.raise_for_status()
