import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_url_for_book(book_id):
    return f'https://tululu.org/txt.php?id={book_id}'


def get_book_title(book_id):
    book_url = f'https://tululu.org/b{book_id}/'
    response = requests.get(book_url)
    if not check_for_redirect(response):
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.find('div', id='content').find('h1').text.split('::')
        return f'{book_id}.{title[0].strip()}'


def download_txt(url, filename, folder='books/'):
    valid_filename = f'{sanitize_filename(filename)}.txt'
    book_path = os.path.join(folder, valid_filename)
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, verify=True)
    if not check_for_redirect(response):
        with open(book_path, 'w') as f:
            f.write(response.text)


def load_books(books_count=10):
    for i in range(1, books_count + 1):
        url = get_url_for_book(i)
        try:
            filename = get_book_title(i)
            download_txt(url, filename)
        except requests.HTTPError:
            continue


load_books()