from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Настройка опций Chrome
options = Options()
options.add_argument("--no-sandbox")  # Устраняет проблемы с правами доступа
options.add_argument("--disable-dev-shm-usage")  # Устраняет проблемы с памятью в контейнерах
options.add_argument("--disable-gpu")  # Отключение GPU (полезно для headless режима)
options.add_argument("--headless")  # Запуск без интерфейса браузера
options.add_argument("--remote-debugging-port=9222")  # Включает отладку

# Установка драйвера
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Переход на сайт
    driver.get("https://freelance.habr.com/tasks")
    driver.implicitly_wait(10)

    # Сбор данных
    titles = driver.find_elements("class name", "task__title")

    # Сохранение заголовков
    with open("titles.txt", "w", encoding="utf-8") as file:
        for title in titles:
            file.write(title.text.strip() + "\n")

finally:
    # Закрытие браузера
    driver.quit()
