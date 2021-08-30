import os
import argparse
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


HOST = "https://api-ssl.bitly.com/v4/{}"


def shorten_link(url, secret_token):
    headers = {"Authorization": "Bearer {}".format(secret_token)}
    playload = {"long_url": url}
    response = requests.post(HOST.format("shorten"), headers=headers, json=playload)
    response.raise_for_status()
    total_bitlink = response.json()["link"]
    return total_bitlink


def count_clicks(url, secret_token):
    headers = {"Authorization": "Bearer {}".format(secret_token)}
    response = requests.get(HOST.format("bitlinks/{bitlink}/clicks/summary".format(bitlink=url)),
                            headers=headers)
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count


def is_bitlink(url, secret_token):
    headers = {"Authorization": "Bearer {}".format(secret_token)}
    response = requests.get(HOST.format("bitlinks/{bitlink}".format(bitlink=url)),
                            headers=headers)
    return response.ok


def main():
    parser = argparse.ArgumentParser(description="Сокращение ссылок и подсчет кликов Bitly.")
    parser.add_argument("links", nargs="+", help="Ссылки для сокращения или подсчета. На вход принимается несколько параметров.")
    args = parser.parse_args()
    for link in args.links:
        secret_token = os.getenv("BITLY_TOKEN")
        url = urlparse(link)
        netloc_and_path = "{}{}".format(url.netloc, url.path)
        try:
            if is_bitlink(netloc_and_path, secret_token):
                print("Количество кликов: ", count_clicks(netloc_and_path, secret_token))
            else:
                print("Битлинк: ", shorten_link(url.geturl(), secret_token))
        except requests.exceptions.HTTPError:
            print("Введена некорректная ссылка.")


if __name__ == "__main__":
    load_dotenv()
    main()
