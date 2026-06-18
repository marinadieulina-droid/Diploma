import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class MapPage:
    URL = "https://www.ppl.cz/mapa-vydejnich-mist"
    WIDGET_HOST = (By.CSS_SELECTOR, "ppl-access-point-widget, #pplWidget")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        # Ждем полной загрузки DOM
        WebDriverWait(self.driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")

    def get_shadow_root(self):
        """Всегда получаем свежий shadow_root."""
        host = WebDriverWait(self.driver, 40).until(
            EC.presence_of_element_located(self.WIDGET_HOST)
        )
        return host.shadow_root

    def accept_cookies(self):
        try:
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
            btn.click()
        except:
            pass
        time.sleep(2)

    def click_geolocation_button(self):
        """Улучшенный метод клика с ожиданием и обработкой перекрытий."""
        shadow = self.get_shadow_root()

        # Ждем появления кнопки именно внутри Shadow DOM
        geo_btn = WebDriverWait(shadow, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Zjistit polohu"]'))
        )

        # Используем JS для клика, если элемент перекрыт
        try:
            geo_btn.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", geo_btn)

        print("[SUCCESS] Geolocation button clicked.")