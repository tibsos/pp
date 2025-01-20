import requests
from bs4 import BeautifulSoup

# URL страницы
link = 'https://freelance.habr.com/tasks'

# Получаем HTML-код страницы
check = requests.get(link)
html_content = check.text

# Используем BeautifulSoup для парсинга
soup = BeautifulSoup(html_content, 'html.parser')
titles = soup.find_all('a')

# Открываем файл для записи
for title in titles:
    print(title.get_text(strip=True))