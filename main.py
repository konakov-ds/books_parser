import os
import requests

base_url = 'https://tululu.org/txt.php?id='
books_count = 0
i = 1
books_path = os.path.join(os.getcwd(), 'books')

os.makedirs(books_path, exist_ok=True)

while books_count < 10:
    url = f'{base_url}{i}'
    response = requests.get(url, verify=True)
    if response:
        with open(f'{books_path}/id{i}', 'w') as f:
            f.write(response.text)
            books_count += 1
    i += 1


print(os.listdir(books_path))