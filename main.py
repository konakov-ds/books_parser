import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_soup(book_id):
    book_url = f'https://tululu.org/b{book_id}/'
    response = requests.get(book_url)
    if not check_for_redirect(response):
        return BeautifulSoup(response.text, 'lxml')


def download_txt(url, filename, folder='books/'):
    valid_filename = f'{sanitize_filename(filename)}.txt'
    book_path = os.path.join(folder, valid_filename)
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, verify=True)
    if not check_for_redirect(response):
        with open(book_path, 'w') as f:
            f.write(response.text)


def download_image(book_id, folder='images/'):
    url, img_src = get_book_img(book_id)
    img_name = img_src.split('/')[2]
    img_path = os.path.join(folder, img_name)
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, verify=True)
    if not check_for_redirect(response):
        with open(img_path, 'wb') as f:
            f.write(response.content)


def load_images(books_count=10):
    for i in range(1, books_count + 1):
        try:
            download_image(i)
        except requests.HTTPError:
            continue
    print('Books images download successfully!')


def load_books(books_count=10):
    for i in range(1, books_count + 1):
        url = get_url_for_book(i)
        try:
            filename = get_book_title(i)
            download_txt(url, filename)
        except requests.HTTPError:
            continue
    print('Books download successfully!')


def load_comments(books_count=10):
    for i in range(1, books_count + 1):
        try:
            title = get_book_title(i)
            comments = get_book_comments(i)
            print(f'{title}')
            print('\n'.join(comments), end='\n\n')
        except requests.HTTPError:
            continue


def parse_book_page(book_id):

    soup = get_book_soup(book_id)

    head = soup.find('div', id='content').find('h1').text.split('::')
    title = head[0].strip()
    author = head[1].strip()
    genre_find = soup.find('span', class_='d_book').find_all('a')
    genre = ', '.join([genre.text for genre in genre_find])
    img_src = soup.find('div', class_='bookimage').find('img')['src']
    img_url = urljoin('https://tululu.org/', img_src)
    text_url = f'https://tululu.org/txt.php?id={book_id}'

    book_info = {
        'title': title,
        'author': author,
        'genres': genre,
        'img_url': img_url,
        'text_url': text_url
    }

    return book_info


#load_images()
#download_image(5)

print(parse_book_page(1))