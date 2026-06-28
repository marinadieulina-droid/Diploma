import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MapPage:
    """Класс для работы со страницей карты отделений PPL (Page Object Model)."""

    URL = "https://www.ppl.cz/mapa-vydejnich-mist"

    PRIMARY_COOKIE_BTN = (By.ID, "onetrust-accept-btn-handler")
    WIDGET_HOST = (By.CSS_SELECTOR, "ppl-access-point-widget, #pplWidget")

    SEARCH_INPUT_SHADOW = (By.CSS_SELECTOR, "input[type='text'], input.search-input")
    SEARCH_INPUT_FALLBACK = (By.CSS_SELECTOR, "input[placeholder*='Hledejte'], input.search-input")

    def __init__(self, driver):
        self.driver = driver
        self._shadow_root = None

    def open(self):
        self.driver.get(self.URL)
        WebDriverWait(self.driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def get_current_url(self):
        return self.driver.current_url

    def accept_cookies(self):
        try:
            cookie_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.PRIMARY_COOKIE_BTN)
            )
            cookie_btn.click()
        except Exception:
            pass

        # time.sleep намеренно: Shadow DOM не поддерживает EC,
        # виджет отрисовывается асинхронно
        try:
            shadow = self.get_shadow_root()
            time.sleep(1.5)
            buttons = shadow.find_elements(By.CSS_SELECTOR, "button")
            for btn in buttons:
                if "Přijmout" in btn.text or "vše" in btn.text:
                    self.driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1.5)
                    break
        except Exception:
            pass

    def get_shadow_root(self):
        if not self._shadow_root:
            shadow_host = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.WIDGET_HOST)
            )
            self._shadow_root = shadow_host.shadow_root
        return self._shadow_root

    def _wait_and_click_by_text(self, text_substring, timeout=15):
        """time.sleep(0.5) намеренно: ручной цикл поиска в Shadow DOM,
        WebDriverWait не поддерживает EC для Shadow DOM."""
        shadow = self.get_shadow_root()
        end_time = time.monotonic() + timeout
        target = text_substring.lower().replace(" ", "")

        while time.monotonic() < end_time:
            try:
                elements = shadow.find_elements(By.CSS_SELECTOR, "button, span, div, label")
                for el in elements:
                    try:
                        text = el.get_attribute("textContent") or ""
                        if target in text.lower().replace(" ", ""):
                            return el
                    except Exception:
                        continue
            except Exception:
                pass
            time.sleep(0.5)
        raise TimeoutException(f"Не удалось найти элемент с текстом '{text_substring}' в Shadow DOM")

    def get_search_field(self):
        try:
            shadow = self.get_shadow_root()
            return shadow.find_element(*self.SEARCH_INPUT_SHADOW)
        except Exception:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.SEARCH_INPUT_FALLBACK)
            )

    def enter_search_query(self, text):
        search_field = self.get_search_field()
        self.driver.execute_script("arguments[0].click();", search_field)
        self.driver.execute_script("arguments[0].value = '';", search_field)
        search_field.send_keys(text)
        WebDriverWait(self.driver, 5).until(
            lambda d: search_field.get_attribute("value") != ""
        )

    def get_search_field_value(self):
        search_field = self.get_search_field()
        return search_field.get_attribute("value")

    def click_geolocation_button(self):
        """time.sleep намеренно: кнопка в Shadow DOM, WebDriverWait не поддерживает EC."""
        shadow = self.get_shadow_root()
        end_time = time.monotonic() + 20
        while time.monotonic() < end_time:
            buttons = shadow.find_elements(By.CSS_SELECTOR, "button")
            for btn in buttons:
                try:
                    label = btn.get_attribute("aria-label") or ""
                    if label == "Zjistit polohu":
                        self.driver.execute_script("arguments[0].click();", btn)
                        time.sleep(2)
                        return True
                except Exception:
                    continue
            time.sleep(1)
        return False

    def open_filters_panel(self):
        """time.sleep(2) намеренно: Shadow DOM не позволяет отследить
        момент открытия панели через WebDriverWait."""
        filters_btn = self._wait_and_click_by_text("Všech", timeout=12)
        self.driver.execute_script("arguments[0].click();", filters_btn)
        time.sleep(2)

    def expand_typ_mista_category(self):
        """time.sleep(2) намеренно: Shadow DOM не позволяет отследить
        раскрытие категории через WebDriverWait."""
        try:
            typ_mista_el = self._wait_and_click_by_text("Typ místa", timeout=5)
            self.driver.execute_script("arguments[0].click();", typ_mista_el)
            time.sleep(2)
        except TimeoutException:
            pass

    def select_shop_and_box_filters(self):
        """time.sleep(0.5) намеренно: виджет перерисовывает чекбоксы
        асинхронно после каждого клика."""
        shadow = self.get_shadow_root()
        filter_options = shadow.find_elements(
            By.CSS_SELECTOR, "input[type='checkbox'], label, button"
        )

        shop_clicked = False
        box_clicked = False

        for option in filter_options:
            try:
                text_content = option.get_attribute("textContent") or ""
                val_attr = option.get_attribute("value") or ""
                id_attr = option.get_attribute("id") or ""
                full_identity = (text_content + val_attr + id_attr).lower()

                if "shop" in full_identity and not shop_clicked:
                    self.driver.execute_script("arguments[0].click();", option)
                    shop_clicked = True
                    time.sleep(0.5)

                if "box" in full_identity and not box_clicked:
                    self.driver.execute_script("arguments[0].click();", option)
                    box_clicked = True
                    time.sleep(0.5)
            except Exception:
                continue

    def apply_filters(self):
        """time.sleep(2) намеренно: Shadow DOM не позволяет отследить
        обновление результатов после применения фильтров через WebDriverWait."""
        try:
            apply_btn = self._wait_and_click_by_text("Zobrazit", timeout=5)
            self.driver.execute_script("arguments[0].click();", apply_btn)
        except TimeoutException:
            filters_btn = self._wait_and_click_by_text("Všech", timeout=5)
            self.driver.execute_script("arguments[0].click();", filters_btn)
        time.sleep(2)