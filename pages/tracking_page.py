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

    def wait_for_result(self):
        """
        Ожидает появления либо таблицы результатов, либо сообщения об ошибке.
        Используем явное ожидание вместо time.sleep для стабильности.
        """
        try:
            WebDriverWait(self.driver, 15).until(
                lambda d: (
                    d.find_elements(*self.RESULT_TABLE)
                    or d.find_elements(*self.ERROR_MESSAGE)
                )
            )
        except Exception:
            # Если ни один элемент не появился — продолжаем, тест упадёт на assert
            pass

    def get_history(self):
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