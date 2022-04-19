import argparse
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from parsing_utils import check_for_redirect
from parse_tululu_books_by_id import books_downloads

base_url = "https://tululu.org/l55/"


def get_page_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return BeautifulSoup(response.text, 'lxml')


def get_num_pages(url):
    soup = get_page_soup(url)
    selector = '.npage:last-child'
    return int(soup.select_one(selector).text)


def get_books_ids(base_url, start_page=1, end_page=get_num_pages(base_url)):
    selector = '.d_book [href*="/b"]'
    books_ids = []
    for page in range(start_page, end_page):
        page_url = urljoin(base_url, str(page))
        soup = get_page_soup(page_url)
        page_books_ids = [
            book.get('href')[2:-1] for book in soup.select(selector)
        ]
        books_ids.extend(set(page_books_ids))
    return books_ids


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--start_page', type=int, default=1)
    parser.add_argument('--end_page', type=int)
    parser.add_argument('--dest_folder')
    parser.add_argument('--json_path')
    parser.add_argument('--skip_img', type=bool)
    parser.add_argument('--skip_txt', type=bool)

    args = parser.parse_args()
    books_ids = get_books_ids(base_url, args.start_page, args.end_page)
    books_downloads(
        books_ids,
        dest_folder=args.dest_folder,
        json_path=args.json_path,
        skip_img=args.skip_img,
        skip_txt=args.skip_txt
    )
