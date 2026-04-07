"""Консольный вывод информации о стране с restcountries.com и цветами (colorama)."""

from __future__ import annotations

import json
import sys
from typing import Any
from urllib.parse import quote

import requests
from colorama import Fore, Style, init

import http_client

REST_COUNTRIES_BASE = "https://restcountries.com/v3.1/name"

init(autoreset=True)


def _label(text: str) -> str:
    return f"{Fore.YELLOW}{Style.BRIGHT}{text}{Style.RESET_ALL}"


def _value(text: str) -> str:
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"


def _header(text: str) -> str:
    return f"\n{Fore.CYAN}{Style.BRIGHT}{'═' * 52}{Style.RESET_ALL}\n{Fore.CYAN}{Style.BRIGHT}  {text}{Style.RESET_ALL}\n{Fore.CYAN}{Style.BRIGHT}{'═' * 52}{Style.RESET_ALL}\n"


def _dim(text: str) -> str:
    return f"{Fore.LIGHTBLACK_EX}{text}{Style.RESET_ALL}"


def _error(text: str) -> None:
    print(f"{Fore.RED}{Style.BRIGHT}{text}{Style.RESET_ALL}")


def _join_list(items: list[Any] | None, sep: str = ", ") -> str:
    if not items:
        return "—"
    return sep.join(str(x) for x in items)


def _format_currencies(currencies: dict[str, Any] | None) -> str:
    if not currencies:
        return "—"
    parts = []
    for code, data in currencies.items():
        if isinstance(data, dict):
            name = data.get("name", "")
            symbol = data.get("symbol", "")
            parts.append(f"{code}: {name} ({symbol})" if symbol else f"{code}: {name}")
        else:
            parts.append(f"{code}: {data}")
    return "; ".join(parts)


def _format_languages(langs: dict[str, str] | None) -> str:
    if not langs:
        return "—"
    return ", ".join(f"{code} — {name}" for code, name in langs.items())


def fetch_country_by_name(name: str) -> tuple[list[dict[str, Any]] | None, str | None]:
    path = quote(name.strip(), safe="")
    url = f"{REST_COUNTRIES_BASE}/{path}"
    try:
        response = http_client.get(url, timeout=15)
    except requests.RequestException as exc:
        return None, str(exc)

    if response.status_code == 404:
        return None, "Страна не найдена (404)."
    if not http_client.ok(response):
        return None, f"Ошибка HTTP {response.status_code}."

    try:
        data = response.json()
    except json.JSONDecodeError:
        return None, "Не удалось разобрать ответ как JSON."

    if not isinstance(data, list) or not data:
        return None, "Пустой или неожиданный ответ API."

    return data, None


def print_country_card(country: dict[str, Any]) -> None:
    name_block = country.get("name") or {}
    common = name_block.get("common", "—")
    official = name_block.get("official", "—")

    capital = _join_list(country.get("capital"))
    region = country.get("region") or "—"
    subregion = country.get("subregion") or "—"
    population = country.get("population")
    area = country.get("area")
    borders = _join_list(country.get("borders"))
    timezones = _join_list(country.get("timezones"))
    cca2 = country.get("cca2") or "—"
    cca3 = country.get("cca3") or "—"
    fifa = country.get("fifa") or "—"
    flag_emoji = country.get("flag") or ""

    currencies = _format_currencies(country.get("currencies"))
    languages = _format_languages(country.get("languages"))

    maps_block = country.get("maps") or {}
    google_maps = maps_block.get("googleMaps", "")

    flags_block = country.get("flags") or {}
    flag_png = flags_block.get("png", "")

    print(_header(f"{flag_emoji}  {common}".strip()))

    def row(lbl: str, val: str) -> None:
        print(f"  {_label(lbl):<22} {_value(val)}")

    row("Официально", str(official))
    row("Столица", str(capital))
    row("Регион", f"{region} ({subregion})")
    row("Население", f"{population:,}" if isinstance(population, int) else str(population or "—"))
    row("Площадь км²", f"{area:,.0f}" if isinstance(area, (int, float)) else str(area or "—"))
    row("Коды", f"{cca2} / {cca3} (FIFA: {fifa})")
    row("Валюты", currencies)
    row("Языки", languages)
    row("Соседи (коды)", borders)
    row("Часовые пояса", timezones)
    if google_maps:
        row("Карта (Google)", google_maps)
    if flag_png:
        row("Флаг (PNG)", flag_png)

    print()


def main() -> None:
    print(_dim("Данные: https://restcountries.com/"))
    country = input(f"{Fore.MAGENTA}Введите название страны: {Style.RESET_ALL}").strip()
    if not country:
        _error("Название не может быть пустым.")
        sys.exit(1)

    countries, err = fetch_country_by_name(country)
    if err:
        _error(err)
        sys.exit(1)

    assert countries is not None

    print_country_card(countries[0])

    if len(countries) > 1:
        others = [c.get("name", {}).get("common", "?") for c in countries[1:]]
        print(
            _dim(
                f"Ещё совпадений: {len(countries) - 1} — {', '.join(others)}"
            )
        )


if __name__ == "__main__":
    main()
