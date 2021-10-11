import os
import requests

base_url = 'https://tululu.org/txt.php?id='
books_path = os.path.join(os.getcwd(), 'books')
os.makedirs(books_path, exist_ok=True)


def load_books(url, books_count=11):
    for i in range(1, books_count):
        url = f'{base_url}{i}'
        response = requests.get(url, verify=True)
        if response:
            with open(f'{books_path}/id{i}', 'w') as f:
                f.write(response.text)


print(sorted(os.listdir(books_path)))