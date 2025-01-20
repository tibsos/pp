import requests
from bs4 import BeautifulSoup

# URL страницы
link = 'https://freelance.habr.com/tasks'

# Получаем HTML-код страницы
check = requests.get(link)
html_content = check.text

# Используем BeautifulSoup для парсинга
soup = BeautifulSoup(html_content, 'html.parser')

# Находим все теги, содержащие заголовки
titles = soup.find_all('a', class_='task__title')

# Открываем файл для записи
with open('titles.txt', 'w', encoding='utf-8') as file:
    for title in titles:
        file.write(title.get_text(strip=True) + '\n')

print("Заголовки сохранены в файл 'titles.txt'")