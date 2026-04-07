import json
from urllib.parse import quote

import requests

REST_COUNTRIES_BASE = "https://restcountries.com/v3.1/name"


def send_get_request() -> None:
    url = input("Введите URL для GET запроса: ").strip()
    if not url:
        print("URL не может быть пустым.")
        return

    try:
        response = requests.get(url, timeout=10)
        print(f"\nСтатус: {response.status_code}")
        print("Ответ:")
        print(response.text)
    except requests.RequestException as error:
        print(f"Ошибка GET запроса: {error}")


def send_post_request() -> None:
    url = input("Введите URL для POST запроса: ").strip()
    if not url:
        print("URL не может быть пустым.")
        return

    payload_raw = input(
        "Введите JSON-тело (например {\"name\":\"Alex\"}) или оставьте пустым: "
    ).strip()

    payload = {}
    if payload_raw:
        try:
            payload = json.loads(payload_raw)
        except json.JSONDecodeError:
            print("Некорректный JSON.")
            return

    try:
        response = requests.post(url, json=payload, timeout=10)
        print(f"\nСтатус: {response.status_code}")
        print("Ответ:")
        print(response.text)
    except requests.RequestException as error:
        print(f"Ошибка POST запроса: {error}")


def send_restcountries_by_name_request() -> None:
    country = input("Введите название страны (например Germany, France): ").strip()
    if not country:
        print("Название не может быть пустым.")
        return

    path = quote(country, safe="")
    url = f"{REST_COUNTRIES_BASE}/{path}"

    try:
        response = requests.get(url, timeout=10)
        print(f"\nURL: {url}")
        print(f"Статус: {response.status_code}")
        print("Ответ:")
        print(response.text)
    except requests.RequestException as error:
        print(f"Ошибка GET запроса: {error}")


def main() -> None:
    while True:
        print("\n--- Меню ---")
        print("1 - GET (произвольный URL)")
        print("2 - POST (произвольный URL)")
        print("3 - REST Countries: страна по имени (restcountries.com)")
        print("0 - Выход")
        choice = input("Ваш выбор: ").strip()

        if choice == "0":
            print("До свидания.")
            break
        if choice == "1":
            send_get_request()
        elif choice == "2":
            send_post_request()
        elif choice == "3":
            send_restcountries_by_name_request()
        else:
            print("Неверный выбор. Введите 0, 1, 2 или 3.")


if __name__ == "__main__":
    main()
