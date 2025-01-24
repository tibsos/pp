import requests
from bs4 import BeautifulSoup
import time
from .models import Order  # Import your Order model from Django app

# URL страницы
link = 'https://freelance.habr.com/tasks'

while True:
    # Получаем HTML-код страницы
    check = requests.get(link)
    html_content = check.text

    # Используем BeautifulSoup для парсинга
    soup = BeautifulSoup(html_content, 'html.parser')

    # Находим все элементы с классом .content-list__item
    content_list_items = soup.find_all(class_='content-list__item')

    print(content_list_items)

    # Обрабатываем каждый элемент
    for item in content_list_items:
        # Находим элементы с классом .task__title внутри каждого .content-list__item
        task_title = item.find(class_='task__title')
        if task_title:
            # Получаем ссылку (href) из тега <a>
            task_link = task_title.find('a')
            if task_link:
                href = task_link.get('href')
                full_link = 'https://freelance.habr.com' + href
                title = task_title.get_text(strip=True)
                
                # Печатаем ссылку
                print(f"New task found: {title} - {full_link}")
                
                # Сохраняем данные в базу данных Django
                order, created = Order.objects.get_or_create(
                    link=full_link,  # Сохраняем ссылку как уникальное поле
                    defaults={'title': title}  # Добавляем заголовок задачи
                )
                if created:
                    print(f"New order created: {title}")
                else:
                    print(f"Order already exists: {title}")

    # Задержка на 60 секунд
    time.sleep(30)