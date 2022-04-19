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

    head = soup.find('div', id='content').find('h1').text.split('::')
    title, author = [h.strip() for h in head]
    genre = soup.find('span', class_='d_book').find_all('a')
    genre = ', '.join([genre.text for genre in genre])
    comments = soup.find_all('div', class_='texts')
    comments = [comment.find('span').text for comment in comments]
    guid = uuid.uuid4().hex
    img_src = soup.find('div', class_='bookimage').find('img')['src']
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
