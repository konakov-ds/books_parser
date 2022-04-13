import argparse
import json
import os
import uuid
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

base_url = "https://tululu.org/images/"


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_soup(book_id):
    book_url = f'https://tululu.org/b{book_id}/'
    response = requests.get(book_url)
    response.raise_for_status()
    check_for_redirect(response)
    return BeautifulSoup(response.text, 'lxml')


def download_txt(book_id, filename, guid, folder='books/', dest_folder=None):
    if dest_folder:
        folder = f'{dest_folder}/{folder}'
    url = 'https://tululu.org/txt.php'
    params = {'id': book_id}
    os.makedirs(folder, exist_ok=True)
    valid_filename = f'{sanitize_filename(filename)}_{guid}.txt'
    book_path = os.path.join(folder, valid_filename)
    response = requests.get(url, params=params, verify=True)
    response.raise_for_status()
    check_for_redirect(response)
    with open(book_path, 'w') as f:
        f.write(response.text)


def download_image(url, src, guid,  folder='images/', dest_folder=None):
    if dest_folder:
        folder = f'{dest_folder}/{folder}'
    os.makedirs(folder, exist_ok=True)
    img_path = urljoin(folder, f'{guid}_{src.split("/")[2]}')
    response = requests.get(url, verify=True)
    response.raise_for_status()
    check_for_redirect(response)
    with open(img_path, 'wb') as f:
        f.write(response.content)


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


def books_downloads(
        books_ids,
        dest_folder='parse_results/',
        json_path=None,
        skip_txt=False,
        skip_img=False
):
    if dest_folder:
        os.makedirs(dest_folder, exist_ok=True)
    books_info = []
    for book_id in books_ids:
        try:
            book_info = parse_book_page(book_id)
            books_info.append(book_info)
            guid = book_info['guid']
            if not skip_txt:
                download_txt(
                    book_info['book_id'],
                    book_info['title'],
                    guid=guid,
                    dest_folder=dest_folder
                )
                print(f'Book {book_info["book_id"]} download successfully!')
            if 'nopic.gif' in book_info['img_src']:
                guid = ''
            if not skip_img:
                download_image(
                    book_info['img_url'],
                    book_info['img_src'],
                    guid=guid,
                    dest_folder=dest_folder
                )
                print(f'Img book {book_info["book_id"]} download successfully!')

        except requests.HTTPError:
            continue

    if dest_folder and json_path:
        json_path = f'{dest_folder}/{json_path}'
        os.makedirs(json_path, exist_ok=True)
    elif dest_folder:
        json_path = dest_folder
    elif json_path:
        os.makedirs(json_path, exist_ok=True)
    else:
        json_path = ''

    with open(f'{json_path}/books_info.json', 'w', encoding='utf8') as f:
        json.dump(books_info, f, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id', type=int, default=1)
    parser.add_argument('--end_id', type=int, default=10)
    args = parser.parse_args()

    books_downloads(args.start_id, args.end_id)
