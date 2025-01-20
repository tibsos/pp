import requests
from bs4 import BeautifulSoup

# URL страницы
link = 'https://freelance.habr.com/tasks'

# Получаем HTML-код страницы
check = requests.get(link)
html_content = check.text

# Используем BeautifulSoup для парсинга
soup = BeautifulSoup(html_content, 'html.parser')

# Находим все элементы с классом .content-list__item
content_list_items = soup.find_all(class_='content-list__item')

# Открываем файл для записи
with open('titles.txt', 'w', encoding='utf-8') as file:
    for item in content_list_items:
        # Находим элементы с классом .task__title внутри каждого .content-list__item
        task_title = item.find(class_='task__title')
        if task_title:
            # Находим тег <a> внутри .task__title и извлекаем его текст или ссылку
            a_tag = task_title.find('a')
            if a_tag:
                # Извлекаем текст из тега <a>
                file.write(a_tag.get_text(strip=True) + '\n')
                print(a_tag.get_text(strip=True))  # Выводим в консоль
