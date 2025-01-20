from webdriver_manager.chrome import ChromeDriverManager

# Получение пути к ChromeDriver
webdriver_path = ChromeDriverManager().install()
print(f"Путь к веб-драйверу: {webdriver_path}")