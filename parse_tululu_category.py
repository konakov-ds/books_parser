import argparse
import os
import uuid
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from main import check_for_redirect, books_downloads

base_url = "https://tululu.org/l55/"


def get_page_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return BeautifulSoup(response.text, 'lxml')


def get_books_ids(base_url, num_pages=4):
    selector = '.d_book [href*="/b"]'
    books_ids = []
    for page in range(1, num_pages + 1):
        page_url = urljoin(base_url, str(page))
        soup = get_page_soup(page_url)
        page_books_ids = [
            book.get('href')[2:-1] for book in soup.select(selector)
        ]
        books_ids.extend(set(page_books_ids))
    return books_ids


if __name__ == '__main__':
    books_ids = get_books_ids(base_url)
    books_downloads(books_ids)
