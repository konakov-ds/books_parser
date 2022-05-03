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

    try:
        books_info = get_books_info(books_info='books_info.json')
        books_pages = list(chunked(books_info, books_per_page))
        num_pages = len(books_pages)
        Path('pages').mkdir(parents=True, exist_ok=True)

        for page, books in enumerate(books_pages, start=1):
            rows = chunked(books, 2)
            rendered_page = template.render(rows=rows, page=page, num_pages=num_pages)

            with open(f'pages/index{page}.html', 'w', encoding="utf8") as file:
                file.write(rendered_page)

    except TypeError:
        print('Что-то пошло не так')


render()
server = Server()
server.watch('template.html', render)
server.serve(root='./pages/', default_filename='index1.html')
