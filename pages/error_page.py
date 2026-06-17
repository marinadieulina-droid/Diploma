class ErrorPage:
    """Класс для работы со страницами ошибок (404 Not Found)."""

    # Базовый URL и заведомо несуществующий эндпоинт
    INVALID_URL = "https://www.ppl.cz/non-existing-page"

    def __init__(self, driver):
        """
        Конструктор класса страницы ошибки.
        :param driver: Экземпляр WebDriver.
        """
        self.driver = driver

    def open_invalid_page(self):
        """Открывает несуществующую страницу на сайте для вызова ошибки 404."""
        self.driver.get(self.INVALID_URL)

    def get_title(self):
        """Возвращает заголовок вкладки браузера для проверки."""
        return self.driver.title