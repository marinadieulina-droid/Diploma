import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class MapPage:
    """Класс для работы со страницей карты отделений PPL (Page Object Model)."""

    URL = "https://www.ppl.cz/mapa-vydejnich-mist"

    # Стандартные локаторы на странице
    PRIMARY_COOKIE_BTN = (By.ID, "onetrust-accept-btn-handler")
    WIDGET_HOST = (By.CSS_SELECTOR, "ppl-access-point-widget, #pplWidget")

    # Локаторы для поиска (внутри Shadow DOM и запасной снаружи)
    SEARCH_INPUT_SHADOW = (By.CSS_SELECTOR, "input[type='text'], input.search-input")
    SEARCH_INPUT_FALLBACK = (By.CSS_SELECTOR, "input[placeholder*='Hledejte'], input.search-input")

    def __init__(self, driver):
        """Конструктор класса страницы карты."""
        self.driver = driver
        self._shadow_root = None  # Сюда сохраним shadow_root после его активации

    def open(self):
        """Открывает страницу с картой."""
        self.driver.get(self.URL)

    def get_current_url(self):
        """Возвращает текущий URL браузера."""
        return self.driver.current_url

    def accept_cookies(self):
        """Закрывает cookie-баннеры (глобальный и внутри виджета)."""
        # 1. Основные куки сайта
        try:
            cookie_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.PRIMARY_COOKIE_BTN)
            )
            cookie_btn.click()
            print("[SUCCESS] Primary cookies accepted.")
        except Exception:
            pass

        # 2. Вторичные куки внутри виджета
        try:
            shadow = self.get_shadow_root()
            time.sleep(1.5)
            buttons = shadow.find_elements(By.CSS_SELECTOR, "button")
            for btn in buttons:
                if "Přijmout" in btn.text or "vše" in btn.text:
                    self.driver.execute_script("arguments[0].click();", btn)
                    print("[SUCCESS] Secondary cookies inside Shadow DOM accepted.")
                    time.sleep(1.5)
                    break
        except Exception:
            pass

    def get_shadow_root(self):
        """Возвращает и кэширует shadow_root карты стандартным методом Selenium 4."""
        if not self._shadow_root:
            shadow_host = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.WIDGET_HOST)
            )
            self._shadow_root = shadow_host.shadow_root
        return self._shadow_root

    def _wait_and_click_by_text(self, text_substring, timeout=15):
        """Внутренний вспомогательный метод поиска элемента по тексту внутри Shadow DOM."""
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

    # --- Новые методы для работы с поисковой строкой ---

    def get_search_field(self):
        """Находит и возвращает инпут поиска, скрытый внутри Shadow DOM (или берет fallback)."""
        try:
            shadow = self.get_shadow_root()
            # Пытаемся найти инпут внутри Shadow DOM
            return shadow.find_element(*self.SEARCH_INPUT_SHADOW)
        except Exception:
            print("[WARNING] Поиск инпута в Shadow DOM не удался, ищем в глобальном DOM...")
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.SEARCH_INPUT_FALLBACK)
            )

    def enter_search_query(self, text):
        """Безопасно кликает, очищает поле и вводит поисковый запрос (город или индекс)."""
        search_field = self.get_search_field()
        # Кликаем и очищаем поле через JavaScript, чтобы избежать перекрытия слоев
        self.driver.execute_script("arguments[0].click();", search_field)
        self.driver.execute_script("arguments[0].value = '';", search_field)
        search_field.send_keys(text)
        time.sleep(0.5)

    def get_search_field_value(self):
        """Возвращает текущий текст, введенный в поле поиска."""
        search_field = self.get_search_field()
        return search_field.get_attribute("value")

    # --- Методы из предыдущего теста (сохраняем их здесь) ---

    def click_geolocation_button(self):
        """Находит и нажимает кнопку геолокации внутри Shadow DOM."""
        shadow = self.get_shadow_root()
        geolocation_button = WebDriverWait(self.driver, 10).until(
            lambda d: shadow.find_element(By.CSS_SELECTOR, 'button[aria-label="Zjistit polohu"]')
        )
        assert geolocation_button.is_displayed(), "Кнопка геолокации не видна"
        self.driver.execute_script("arguments[0].click();", geolocation_button)
        time.sleep(2)

    def open_filters_panel(self):
        """Открывает шторку всех фильтров."""
        filters_btn = self._wait_and_click_by_text("Všech", timeout=12)
        self.driver.execute_script("arguments[0].click();", filters_btn)
        time.sleep(2)

    def expand_typ_mista_category(self):
        """Раскрывает категорию фильтров 'Typ místa'."""
        try:
            typ_mista_el = self._wait_and_click_by_text("Typ místa", timeout=5)
            self.driver.execute_script("arguments[0].click();", typ_mista_el)
            time.sleep(2)
        except TimeoutException:
            print("[INFO] Категория 'Typ místa' не найдена. Продолжаем.")

    def select_shop_and_box_filters(self):
        """Находит интерактивные чекбоксы фильтров и активирует Shop и Box."""
        shadow = self.get_shadow_root()
        filter_options = shadow.find_elements(By.CSS_SELECTOR, "input[type='checkbox'], label, button")

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
        """Нажимает кнопку 'Zobrazit' для применения выбранных фильтров."""
        try:
            apply_btn = self._wait_and_click_by_text("Zobrazit", timeout=5)
            self.driver.execute_script("arguments[0].click();", apply_btn)
        except TimeoutException:
            filters_btn = self._wait_and_click_by_text("Všech", timeout=5)
            self.driver.execute_script("arguments[0].click();", filters_btn)
        time.sleep(2)