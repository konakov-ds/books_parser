import json
import os
from urllib.parse import urljoin
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

BOOKS_DIR = './dest/'


def process_book_info(books_info='books_info.json'):
    with open(urljoin(BOOKS_DIR, books_info)) as f:
        books = json.load(f)

    books_images_src = [
        book[:book.find('_')] for book in os.listdir(urljoin(BOOKS_DIR, 'images/'))
    ]
    for book in books:
        src_index = None
        guid = book['guid']
        if guid in books_images_src:
            src_index = books_images_src.index(guid)
        book['img_src'] = urljoin(
            urljoin(BOOKS_DIR, 'images/'),
            '_nopic.gif'
        )
        if src_index:
            book['img_src'] = urljoin(
                urljoin(BOOKS_DIR, 'images/'),
                os.listdir(urljoin(BOOKS_DIR, 'images/'))[src_index]
            )
    return books


books_info = process_book_info()

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(books_info=books_info)


with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
