import argparse
import os
import uuid
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_soup(book_id):
    book_url = f'https://tululu.org/b{book_id}/'
    response = requests.get(book_url)
    if not check_for_redirect(response):
        return BeautifulSoup(response.text, 'lxml')


def download_txt(book_id, filename, guid, folder='books/'):
    url = 'https://tululu.org/txt.php'
    params = {'id': book_id}
    os.makedirs(folder, exist_ok=True)
    valid_filename = f'{sanitize_filename(filename)}_{guid}.txt'
    book_path = os.path.join(folder, valid_filename)
    response = requests.get(url, params=params, verify=True)
    if not check_for_redirect(response):
        with open(book_path, 'w') as f:
            f.write(response.text)


def download_image(url, src, guid, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    img_path = os.path.join(folder, f'{guid}_{src}')
    response = requests.get(url, verify=True)
    if not check_for_redirect(response):
        with open(img_path, 'wb') as f:
            f.write(response.content)


def parse_book_page(book_id):
    soup = get_book_soup(book_id)

    head = soup.find('div', id='content').find('h1').text.split('::')
    head = [h.strip() for h in head]
    title, author = head
    genre_find = soup.find('span', class_='d_book').find_all('a')
    genre = ', '.join([genre.text for genre in genre_find])
    comments_find = soup.find_all('div', class_='texts')
    comments = [comment.find('span').text for comment in comments_find]

    img_src = soup.find('div', class_='bookimage').find('img')['src'].split('/')[2]
    img_url = urljoin('https://tululu.org/', img_src)

    book_info = {
        'title': title,
        'author': author,
        'genres': genre,
        'comments': comments,
        'img_src': img_src,
        'img_url': img_url,
        'book_id': book_id
    }

    return book_info


def books_downloads(start_id, end_id):
    for book_id in range(start_id, end_id + 1):
        try:
            book_info = parse_book_page(book_id)
            guid = uuid.uuid4().hex

            download_txt(
                book_info['book_id'],
                book_info['title'],
                guid=guid
            )
            if book_info['img_src'] == 'nopic.gif':
                guid = ''
            download_image(
                book_info['img_url'],
                book_info['img_src'],
                guid=guid
            )
            print(f'Book {book_info["title"]} download successfully!')
        except requests.HTTPError:
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id', type=int, default=1)
    parser.add_argument('--end_id', type=int, default=10)
    args = parser.parse_args()

    books_downloads(args.start_id, args.end_id)