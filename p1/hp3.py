from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Настройка опций Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в фоновом режиме (без окна)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Отключение автоматизации
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Настройка Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Переход на сайт
url = "https://freelance.habr.com/tasks"
print(f"Переход на сайт: {url}")
driver.get(url)

# Даем странице время для загрузки
driver.implicitly_wait(10)

# Получение заголовков
titles = driver.find_elements(By.CLASS_NAME, 'task__title')

# Сохраняем заголовки в файл
with open('titles.txt', 'w', encoding='utf-8') as file:
    for title in titles:
        file.write(title.text.strip() + '\n')

# Закрытие браузера
driver.quit()

print("Заголовки сохранены в файл 'titles.txt'")
