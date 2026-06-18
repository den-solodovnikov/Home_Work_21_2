# Импорт встроенной библиотеки для работы веб-сервера
from http.server import HTTPServer, BaseHTTPRequestHandler

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """
    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        self.send_response(200)  # Отправка кода ответа
        self.send_header("Content-type", "text/html")  # Отправка типа данных, который будет передаваться
        self.end_headers()  # Завершение формирования заголовков ответа

        with open("contact.html", "r", encoding="utf-8") as f:
            page_html = f.read()
            self.wfile.write(bytes(page_html, "utf-8"))  # Тело ответа

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов """
        content_length = int(self.headers.get("Content-Length", 0))

        # Считываем тело запроса в виде байтов
        post_data = self.rfile.read(content_length)

        # Печатаем принятые данные в консоль
        print(f"Получены данные (raw): {post_data}")

        # Попытка декодировать для более удобного чтения
        try:
            print(f"Декодированные данные: {post_data.decode('utf-8')}")
        except UnicodeDecodeError:
            print("Данные не являются текстовыми (например, файл или бинарные данные)")

        # Отправляем ответ клиенту (код 200)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"POST request processed successfully!")


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Старт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
