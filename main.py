import json
from urllib.parse import quote

import requests

import http_client

REST_COUNTRIES_BASE = "https://restcountries.com/v3.1/name"
DOG_CEO_RANDOM_IMAGE = "https://dog.ceo/api/breeds/image/random"


def send_get_request() -> None:
    url = input("Введите URL для GET запроса: ").strip()
    if not url:
        print("URL не может быть пустым.")
        return

    try:
        response = http_client.get(url)
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
        response = http_client.post(url, json=payload)
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
        response = http_client.get(url)
        print(f"\nURL: {url}")
        print(f"Статус: {response.status_code}")
        print("Ответ:")
        print(response.text)

        if http_client.ok(response):
            try:
                data = response.json()
            except json.JSONDecodeError:
                print("\n(Не удалось разобрать JSON для доп. полей.)")
            else:
                item = None
                if isinstance(data, list) and data:
                    item = data[0]
                elif isinstance(data, dict):
                    item = data
                if item is not None:
                    alt = item.get("altSpellings")
                    if isinstance(alt, list):
                        alt_str = ", ".join(str(x) for x in alt)
                    else:
                        alt_str = str(alt) if alt is not None else "—"
                    week_start = item.get("startOfWeek")
                    week_str = str(week_start) if week_start is not None else "—"
                    print("\nНазвание страны:", alt_str)
                    print("Начало недели:", week_str)
    except requests.RequestException as error:
        print(f"Ошибка GET запроса: {error}")


def send_random_dog_image_request() -> None:
    try:
        response = http_client.get(DOG_CEO_RANDOM_IMAGE)
        print(f"\nСтатус: {response.status_code}")
        if not http_client.ok(response):
            print("Ответ:", response.text)
            return
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("Не удалось разобрать ответ как JSON.")
            return
        image_url = data.get("message") if isinstance(data, dict) else None
        if image_url:
            print("Ссылка на изображение:", image_url)
        else:
            print("Ответ:", response.text)
    except requests.RequestException as error:
        print(f"Ошибка GET запроса: {error}")


def main() -> None:
    while True:
        print("\n--- Меню ---")
        print("1 - GET (произвольный URL)")
        print("2 - POST (произвольный URL)")
        print("3 - REST Countries: страна по имени (restcountries.com)")
        print("4 - Случайная собака (dog.ceo)")
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
        elif choice == "4":
            send_random_dog_image_request()
        else:
            print("Неверный выбор. Введите 0, 1, 2, 3 или 4.")


if __name__ == "__main__":
    main()
