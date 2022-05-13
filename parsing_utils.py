import json
import os
from pathlib import Path

import requests
import uuid
from bs4 import BeautifulSoup
from urllib.parse import urljoin


base_url = "https://tululu.org/l55/"
CONTENT_DIR = '../dest/'


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_soup(book_id):
    book_url = f'https://tululu.org/b{book_id}/'
    response = requests.get(book_url)
    response.raise_for_status()
    check_for_redirect(response)
    return BeautifulSoup(response.text, 'lxml')


def parse_book_page(book_id):
    soup = get_book_soup(book_id)
    h1_selector = '#content h1'
    head = soup.select_one(h1_selector).text.split('::')
    title, author = [h.strip() for h in head]
    book_selector = 'span.d_book a'
    genre = soup.select(book_selector)
    genre = [genre.text for genre in genre]

    comment_selector = '.texts span'
    comments = soup.select(comment_selector)
    comments = [comment.text for comment in comments]
    guid = uuid.uuid4().hex
    img_selector = '.bookimage [src]'
    img_src = soup.select_one(img_selector)['src']
    img_url = urljoin(base_url, img_src)
    book_info = {
        'title': title,
        'author': author,
        'genres': genre,
        'comments': comments,
        'img_src': img_src,
        'img_url': img_url,
        'book_id': book_id,
        'guid': guid
    }

    return book_info

def get_books_info(books_info):
    images = os.listdir('./dest/images/')
    books = os.listdir('./dest/books/')
    try:
        with open(Path('./dest/', books_info)) as f:
            books_info = json.load(f)
        images_paths = [
            image[:image.find('_')] for image in images
        ]
        books_paths = [
            book[book.find('_') + 1: -4] for book in books
        ]
        for book in books_info:
            guid = book['guid']
            book['book_path'] = ''
            if guid in books_paths:
                book_path_index = books_paths.index(guid)
                book['book_path'] = Path(CONTENT_DIR, 'books/', books[book_path_index])
                book['img_src'] = Path(CONTENT_DIR, 'images/', 'nopic.gif')
            if guid in images_paths:
                img_path_index = images_paths.index(guid)
                book['img_src'] = Path(CONTENT_DIR, 'images/', images[img_path_index])
        return books_info
    except OSError:
        print('Проблемы при чтении файла с информацией о книгах')
