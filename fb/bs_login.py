import requests
from bs4 import BeautifulSoup

def authenticate(login, password):
    """Попытка авторизации на указанном сайте с использованием библиотеки requests."""
    url = "https://xenforo.com/community/login/"
    session = requests.Session()

    try:
        # Получение страницы логина для получения CSRF-токена
        response = session.get(url)
        if response.status_code != 200:
            print("Ошибка доступа к странице логина")
            return False

        # Извлечение CSRF-токена
        soup = BeautifulSoup(response.text, 'html.parser')
        token_input = soup.find("input", {"name": "_xfToken"})
        login_input = soup.find("input", {"name": "login"})
        password_input = soup.find("input", {"name": "password"})

        if not token_input or not login_input or not password_input:
            print("Не удалось найти необходимые поля формы на странице")
            return False

        token = token_input.get("value")

        # Данные для авторизации
        data = {
            login_input.get("name"): login,
            password_input.get("name"): password,
            token_input.get("name"): token
        }

        # Отправка данных на сервер
        login_response = session.post(url, data=data)
        if login_response.status_code == 200:
            print(login_response.text)
            print("Авторизация успешна!")  # Сообщение при успешной авторизации
            return True
        else:
            print("Ошибка авторизации: проверьте логин и пароль")
            return False
    except Exception as e:
        print(f"Ошибка при авторизации: {e}")
        return False

if __name__ == "__main__":
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    if authenticate(login, password):
        print("Вы успешно вошли в систему!")
    else:
        print("Не удалось войти. Проверьте свои учетные данные.")
