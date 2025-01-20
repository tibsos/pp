from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Настройка Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Запуск без открытия окна браузера

# Запуск браузера через Selenium
webdriver_path = ChromeDriverManager().install()
print(f"Путь к веб-драйверу: {webdriver_path}")

# Инициализация драйвера
driver = webdriver.Chrome(service=Service(webdriver_path))
# Переход на страницу
link = 'https://freelance.habr.com/tasks'
driver.navigate().to("https://selenium.dev")


# Даем время странице загрузиться
time.sleep(3)

# Получаем все тайтлы
titles = driver.find_elements(By.CLASS_NAME, 'task__title')

# Открываем файл для записи
with open('titles.txt', 'w', encoding='utf-8') as file:
    for title in titles:
        file.write(title.text.strip() + '\n')

# Закрытие браузера
driver.quit()

print("Заголовки сохранены в файл 'titles.txt'")
