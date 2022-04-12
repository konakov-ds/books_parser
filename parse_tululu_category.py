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


def get_books_ids(base_url, num_pages=3):
    book_links = []
    for page in range(num_pages):
        page_url = urljoin(base_url, str(page))
        if not page:
            page_url = base_url
        soup = get_page_soup(page_url)
        books = soup.find_all('table', class_='d_book')
        for book in books:
            href = book.find('a', href=True)['href']
            book_links.append(href[2:-1])
    return book_links


if __name__ == '__main__':
    books_ids = get_books_ids(base_url)
    books_downloads(books_ids)
