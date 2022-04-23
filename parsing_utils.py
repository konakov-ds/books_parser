import requests
import uuid
from bs4 import BeautifulSoup
from urllib.parse import urljoin


base_url = "https://tululu.org/l55/"


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
