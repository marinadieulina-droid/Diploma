from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TrackingPage:
    URL = "https://www.ppl.cz/vyhledat-zasilku"

    TRACKING_INPUT = (By.CSS_SELECTOR, "input[type='text']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    COOKIE_BUTTON = (By.ID, "onetrust-accept-btn-handler")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "span.c-help-block")
    RESULT_TABLE = (By.XPATH, "//table[contains(@class,'table-borderless')]")

    # Вкладка "Detail stavu zásilky" реализована через label связанный
    # с radio input — кликаем по label чтобы переключить вкладку
    STATUS_TAB = (By.XPATH, "//label[contains(text(), 'Detail stavu zásilky')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def open(self):
        self.driver.get(self.URL)

    def accept_cookies(self):
        try:
            self.wait.until(EC.element_to_be_clickable(self.COOKIE_BUTTON)).click()
        except Exception:
            pass

    def enter_tracking_number(self, number):
        field = self.wait.until(EC.visibility_of_element_located(self.TRACKING_INPUT))
        field.clear()
        field.send_keys(number)

    def click_search(self):
        self.wait.until(EC.element_to_be_clickable(self.SEARCH_BUTTON)).click()

    def click_status_tab(self):
        """Кликает по вкладке 'Detail stavu zásilky' чтобы открыть таблицу
        с историей статусов. Вкладка реализована через label + radio input,
        поэтому кликаем по label а не по input напрямую."""
        try:
            tab = self.wait.until(EC.element_to_be_clickable(self.STATUS_TAB))
            tab.click()
            # Ждём появления таблицы после клика по вкладке
            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_elements(*self.RESULT_TABLE)
            )
        except Exception:
            pass

    def wait_for_result(self):
        """Ожидает появления блока результатов или сообщения об ошибке."""
        try:
            WebDriverWait(self.driver, 15).until(
                lambda d: (
                    d.find_elements(*self.STATUS_TAB)
                    or d.find_elements(*self.ERROR_MESSAGE)
                )
            )
        except Exception:
            pass

    def get_history(self):
        # Сначала кликаем по вкладке со статусами —
        # по умолчанию открыта вкладка "Detail zásilky", таблицы там нет
        self.click_status_tab()

        rows = self.driver.find_elements(
            By.XPATH,
            "//table[contains(@class,'table-borderless')]//tbody/tr"
        )

        history = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 2:
                history.append({
                    "date": cells[0].get_attribute("textContent").strip(),
                    "status": cells[1].get_attribute("textContent").strip()
                })

        # Убираем дубликаты, сохраняя порядок
        unique_history = []
        for item in history:
            if item not in unique_history:
                unique_history.append(item)
        return unique_history

    def get_error_message(self):
        try:
            return self.driver.find_element(*self.ERROR_MESSAGE).text.strip()
        except Exception:
            return ""