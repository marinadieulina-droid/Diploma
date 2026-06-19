from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomepagePage:
    """Класс, представляющий главную страницу сайта PPL (Page Object Model)."""

    # URL страницы, вынесенный в переменную класса для удобства поддержки
    URL = "https://www.ppl.cz"

    # Локаторы элементов главной страницы
    COOKIE_ACCEPT_BTN = (By.ID, "onetrust-accept-btn-handler")
    LANGUAGE_SELECTOR = (By.CSS_SELECTOR, ".language-selector-select")

    # Локаторы для SEO мета-тегов (Xpath)
    META_DESCRIPTION = (By.XPATH, "//meta[@name='description']")
    OG_TITLE = (By.XPATH, "//meta[@property='og:title']")
    OG_DESCRIPTION = (By.XPATH, "//meta[@property='og:description']")
    OG_URL = (By.XPATH, "//meta[@property='og:url']")

    # Новый локатор: пункты навигационного меню в шапке сайта
    MENU_ITEMS = (By.CSS_SELECTOR, ".navbar__link")

    def __init__(self, driver):
        """
        Конструктор класса.
        :param driver: Экземпляр WebDriver, переданный из теста.
        """
        self.driver = driver

    def open(self):
        """Открывает главную страницу в браузере с помощью сохраненного драйвера."""
        self.driver.get(self.URL)

    def get_title(self):
        """
        Запрашивает у браузера заголовок (title) текущей активной вкладки.
        :return: Строка с текстом заголовка страницы.
        """
        return self.driver.title

    def accept_cookies(self):
        """
        Ожидает появление всплывающего баннера кук и кликает на кнопку согласия.
        Использует явное ожидание (Explicit Wait) до 10 секунд.
        """
        cookie_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN)
        )
        cookie_btn.click()

    def get_selected_language(self):
        select_element = self.driver.find_element(*self.LANGUAGE_SELECTOR)
        language_dropdown = Select(select_element)

        return language_dropdown.first_selected_option.text.strip().lower()

    def switch_language(self, language):
        """
        Переключает язык сайта.
        Поддерживаются значения: 'cs' и 'en'.
        """

        select_element = self.driver.find_element(*self.LANGUAGE_SELECTOR)
        language_dropdown = Select(select_element)

        if language == "en":
            language_dropdown.select_by_value("en_US")
        elif language == "cs":
            language_dropdown.select_by_value("cs_CZ")
        else:
            raise ValueError(
                f"Неподдерживаемый язык: {language}"
            )

    # --- Методы для извлечения мета-тегов ---

    def get_meta_description(self):
        """Находит тег description и возвращает значение его атрибута content."""
        element = self.driver.find_element(*self.META_DESCRIPTION)
        return element.get_attribute("content")

    def get_og_title(self):
        """Находит тег og:title и возвращает значение его атрибута content."""
        element = self.driver.find_element(*self.OG_TITLE)
        return element.get_attribute("content")

    def get_og_description(self):
        """Находит тег og:description и возвращает значение его атрибута content."""
        element = self.driver.find_element(*self.OG_DESCRIPTION)
        return element.get_attribute("content")

    def get_og_url(self):
        """Находит тег og:url и возвращает значение его атрибута content."""
        element = self.driver.find_element(*self.OG_URL)
        return element.get_attribute("content")

    # --- Новый метод для навигационного меню ---

    def get_navigation_links(self):
        """
        Находит все пункты меню и собирает значения их атрибутов 'href'.
        :return: Список (list) строк с URL-адресами ссылок меню.
        """
        elements = self.driver.find_elements(*self.MENU_ITEMS)
        links = []
        for el in elements:
            href = el.get_attribute("href")
            links.append(href)
        return links