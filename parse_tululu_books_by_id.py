import argparse
import json
import os
from urllib.parse import urljoin

import requests
from pathvalidate import sanitize_filename
from parsing_utils import check_for_redirect, parse_book_page

base_url = "https://tululu.org/images/"

def check_book_txt(book_id):
    url = 'https://tululu.org/txt.php'
    params = {'id': book_id}
    try:
        response = requests.get(url, params=params, verify=True)
        response.raise_for_status()
        if not response.text:
            return False
        return True
    except requests.HTTPError:
        return False


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
        if not check_book_txt(book_id):
            continue
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

    books_downloads(range(args.start_id, args.end_id))
