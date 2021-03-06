
# Программа для создания своей онлайн библиотеки

Программа позволяет скачивать текст книги, а также получить дополнительную
информацию (обложку, жанр, комментарии).
Используется ресурс [tululu.org](https://tululu.org/).
Для скачивания книг из определенного диапазона id используйте `parse_tululu_books_by_id`, для скачивания книг из категории фантастика - `parse_tululu_category.py`
Пример реализации на [GitHub Pages](https://konakov-ds.github.io/books_parser/pages/index1.html).

###  Переменные окружения
`parse_tululu_books_by_id`
- start_id, end_id : диапазон id книг для скачивания.  По умолчанию
start_id = 1, end_id = 10
  
`parse_tululu_category.py`
- start_page, end_page : диапазон страниц для скачивания, если не указывать end_page, то будут скачиваться все страницы до последней.
  
`common`

- dest_folder: название папки, в которую будут скачиваться результаты работы скрипта.
- json_path: название папки, в которую будет сохраняться отчет json.
- skip_img: не скачивать обложки книг (по умолчанию False).
- skip_txt: не скачивать тексты книг (по умолчанию False).

###  Зависимости
- Установить зависимости:

   ```
   pip install -r requirements.txt
  ```
###  Запуск скрипта
- Запустить скрипт можно командой:
  
  ```
  python parse_tululu_books_by_id.py --start_id START --end_id END --OTHERS
  ```
  ```
  python parse_tululu_category.py --start_page START --end_page END --OTHERS
  ```
