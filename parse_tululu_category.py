import argparse
import os
import uuid
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from main import check_for_redirect

base_url = "https://tululu.org/l55/"


def get_page_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return BeautifulSoup(response.text, 'lxml')


def get_book_links(base_url):
    soup = get_page_soup(base_url)
    books = soup.find_all('table', class_='d_book')
    book_links = []
    for book in books:
        href = book.find('a', href=True)['href']
        link = urljoin(base_url, href)
        book_links.append(link)
    return book_links


if __name__ == '__main__':
    response = get_book_links(base_url)
    print(response)
