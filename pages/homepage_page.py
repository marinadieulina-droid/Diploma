from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException


class HomepagePage:
    """Класс, представляющий главную страницу сайта PPL (Page Object Model)."""

    URL = "https://www.ppl.cz"

    COOKIE_ACCEPT_BTN = (By.ID, "onetrust-accept-btn-handler")
    LANGUAGE_SELECTOR = (By.CSS_SELECTOR, ".language-selector-select")

    META_DESCRIPTION = (By.XPATH, "//meta[@name='description']")
    OG_TITLE = (By.XPATH, "//meta[@property='og:title']")
    OG_DESCRIPTION = (By.XPATH, "//meta[@property='og:description']")
    OG_URL = (By.XPATH, "//meta[@property='og:url']")

    MENU_ITEMS = (By.CSS_SELECTOR, ".navbar__link")

    # Количество нажатий TAB для достижения кнопки "Track shipment".
    # Значение 5 определено экспериментально по структуре DOM главной страницы:
    # 1 — логотип, 2 — меню «Zásilky», 3 — меню «Služby», 4 — переключатель языка,
    # 5 — кнопка «Track shipment» в шапке.
    # При изменении разметки это значение нужно пересмотреть.
    TAB_PRESSES_TO_TRACK_BUTTON = 5

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)

    def get_title(self):
        return self.driver.title

    def accept_cookies(self):
        cookie_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.COOKIE_ACCEPT_BTN)
        )
        cookie_btn.click()

    def get_selected_language(self):
        """Возвращает выбранный язык, повторяя поиск элемента при его обновлении."""
        for _ in range(3):
            try:
                select_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(self.LANGUAGE_SELECTOR)
                )
                language_dropdown = Select(select_element)
                return language_dropdown.first_selected_option.text.strip().lower()
            except StaleElementReferenceException:
                continue

        raise StaleElementReferenceException(
            "Language selector remained stale after several attempts."
        )

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
            raise ValueError(f"Unsupported language: '{language}'. Use 'cs' or 'en'.")

    def navigate_with_tab(self, presses=None):
        """
        Перемещает фокус по странице клавишей TAB.

        :param presses: количество нажатий TAB.
                        По умолчанию — TAB_PRESSES_TO_TRACK_BUTTON.
        :return: активный элемент после навигации.
        """
        if presses is None:
            presses = self.TAB_PRESSES_TO_TRACK_BUTTON

        body = self.driver.find_element(By.TAG_NAME, "body")
        for _ in range(presses):
            body.send_keys(Keys.TAB)

        return self.driver.switch_to.active_element

    def get_meta_description(self):
        element = self.driver.find_element(*self.META_DESCRIPTION)
        return element.get_attribute("content")

    def get_og_title(self):
        element = self.driver.find_element(*self.OG_TITLE)
        return element.get_attribute("content")

    def get_og_description(self):
        element = self.driver.find_element(*self.OG_DESCRIPTION)
        return element.get_attribute("content")

    def get_og_url(self):
        element = self.driver.find_element(*self.OG_URL)
        return element.get_attribute("content")

    def get_navigation_links(self):
        """
        Возвращает список href всех пунктов навигационного меню.
        """
        elements = self.driver.find_elements(*self.MENU_ITEMS)
        return [el.get_attribute("href") for el in elements]