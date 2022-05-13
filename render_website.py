from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

from parsing_utils import get_books_info


def render(books_per_page=10):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    book_storage = get_books_info(books_info='books_info.json')
    books_chunks = list(chunked(book_storage, books_per_page))
    pages_num = len(books_chunks)
    Path('pages').mkdir(parents=True, exist_ok=True)

    for page, books in enumerate(books_chunks, start=1):
        rows = chunked(books, 2)
        rendered_page = template.render(rows=rows, page=page, num_pages=pages_num)

        with open(f'pages/index{page}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


render()
server = Server()
server.watch('template.html', render)
server.serve(root='./pages/', default_filename='index1.html')
