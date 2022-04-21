import json
import os
from urllib.parse import urljoin
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

BOOKS_DIR = './dest/'


def process_book_info(books_info='books_info.json'):
    images = os.listdir(urljoin(BOOKS_DIR, 'images/'))
    books = os.listdir(urljoin(BOOKS_DIR, 'books/'))

    with open(urljoin(BOOKS_DIR, books_info)) as f:
        books_info = json.load(f)

    books_images_paths = [
        book[:book.find('_')] for book in images
    ]
    books_paths = [
        book[book.find('_') + 1: -4] for book in books
    ]
    print(books_paths)
    for book in books_info:
        img_path_index = None
        guid = book['guid']
        book['book_path'] = ''
        if guid in books_paths:
            book_path_index = books_paths.index(guid)
            book['book_path'] = urljoin(
                    urljoin(BOOKS_DIR, 'books/'),
                    books[book_path_index]
                )
        if guid in books_images_paths:
            img_path_index = books_images_paths.index(guid)
        book['img_src'] = urljoin(
            urljoin(BOOKS_DIR, 'images/'),
            '_nopic.gif'
        )
        if img_path_index:
            book['img_src'] = urljoin(
                urljoin(BOOKS_DIR, 'images/'),
                images[img_path_index]
            )
    return books_info


def render():
    books_info = process_book_info()
    rows = chunked(books_info, 2)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(rows=rows)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


render()
server = Server()
server.watch('template.html', render)
server.serve(root='.')
# server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()
