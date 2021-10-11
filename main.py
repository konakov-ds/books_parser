import os
import requests


books_base_url = 'https://tululu.org/txt.php?id='
books_path = os.path.join(os.getcwd(), 'books')
os.makedirs(books_path, exist_ok=True)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def load_books(books_count=11):
    for i in range(1, books_count):
        url = f'{books_base_url}{i}'
        response = requests.get(url, verify=True)
        try:
            check_for_redirect(response)
            with open(f'{books_path}/id{i}', 'w') as f:
                f.write(response.text)
        except requests.HTTPError:
            continue


load_books()
print(sorted(os.listdir(books_path)))