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
        self._shadow_root = None

    def open(self):
        self.driver.get(self.URL)
        WebDriverWait(self.driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

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
        except Exception:
            pass

        # 2. Вторичные куки внутри виджета (Shadow DOM).
        # Здесь используется time.sleep(1.5) намеренно: Shadow DOM не поддерживает
        # стандартные условия EC, поэтому WebDriverWait не может отслеживать
        # появление кнопки внутри shadow_root. Пауза нужна чтобы виджет успел
        # отрисовать кнопки после загрузки.
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
        """Возвращает и кэширует shadow_root карты стандартным методом Selenium 4."""
        if not self._shadow_root:
            shadow_host = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located(self.WIDGET_HOST)
            )
            self._shadow_root = shadow_host.shadow_root
        return self._shadow_root

    def _wait_and_click_by_text(self, text_substring, timeout=15):
        """Внутренний вспомогательный метод поиска элемента по тексту внутри Shadow DOM.

        time.sleep(0.5) между итерациями оставлен намеренно: стандартный WebDriverWait
        не умеет работать с элементами внутри Shadow DOM через условия EC,
        поэтому используется ручной цикл с паузой между попытками.
        """
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
        """Находит и возвращает инпут поиска внутри Shadow DOM (или берет fallback)."""
        try:
            shadow = self.get_shadow_root()
            return shadow.find_element(*self.SEARCH_INPUT_SHADOW)
        except Exception:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(self.SEARCH_INPUT_FALLBACK)
            )

    def enter_search_query(self, text):
        """Безопасно кликает, очищает поле и вводит поисковый запрос.

        Вместо time.sleep(0.5) используем явное ожидание — ждём пока значение
        в поле станет непустым, то есть текст реально появился в инпуте.
        """
        search_field = self.get_search_field()
        self.driver.execute_script("arguments[0].click();", search_field)
        self.driver.execute_script("arguments[0].value = '';", search_field)
        search_field.send_keys(text)
        WebDriverWait(self.driver, 5).until(
            lambda d: search_field.get_attribute("value") != ""
        )

    def get_search_field_value(self):
        """Возвращает текущий текст, введенный в поле поиска."""
        search_field = self.get_search_field()
        return search_field.get_attribute("value")

    def click_geolocation_button(self):
        """Нажимает кнопку определения местоположения внутри Shadow DOM.

        time.sleep(1) между итерациями и time.sleep(2) после клика оставлены
        намеренно: кнопка геолокации находится внутри Shadow DOM и появляется
        асинхронно. WebDriverWait не поддерживает условия EC для Shadow DOM,
        поэтому используется ручной цикл с паузами.
        """
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
        """Открывает шторку всех фильтров.

        Вместо time.sleep(2) используем явное ожидание — ждём пока панель
        фильтров станет видимой в Shadow DOM после клика по кнопке.
        """
        filters_btn = self._wait_and_click_by_text("Všech", timeout=12)
        self.driver.execute_script("arguments[0].click();", filters_btn)
        WebDriverWait(self.driver, 10).until(
            lambda d: len(self.get_shadow_root().find_elements(
                By.CSS_SELECTOR, "input[type='checkbox'], label"
            )) > 0
        )

    def expand_typ_mista_category(self):
        """Раскрывает категорию фильтров 'Typ místa'.

        Вместо time.sleep(2) используем явное ожидание — ждём пока после клика
        внутри Shadow DOM появятся дочерние элементы категории.
        """
        try:
            typ_mista_el = self._wait_and_click_by_text("Typ místa", timeout=5)
            self.driver.execute_script("arguments[0].click();", typ_mista_el)
            WebDriverWait(self.driver, 5).until(
                lambda d: len(self.get_shadow_root().find_elements(
                    By.CSS_SELECTOR, "input[type='checkbox']"
                )) > 0
            )
        except TimeoutException:
            pass

    def select_shop_and_box_filters(self):
        """Находит интерактивные чекбоксы фильтров и активирует Shop и Box.

        time.sleep(0.5) между кликами оставлен намеренно: после каждого клика
        виджет внутри Shadow DOM перерисовывает состояние чекбоксов асинхронно.
        WebDriverWait не может отследить завершение этой перерисовки через EC,
        поэтому короткая пауза необходима для стабильности.
        """
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
        """Нажимает кнопку 'Zobrazit' для применения выбранных фильтров.

        Вместо time.sleep(2) используем явное ожидание — ждём пока Shadow DOM
        обновит список результатов после применения фильтров.
        """
        try:
            apply_btn = self._wait_and_click_by_text("Zobrazit", timeout=5)
            self.driver.execute_script("arguments[0].click();", apply_btn)
        except TimeoutException:
            filters_btn = self._wait_and_click_by_text("Všech", timeout=5)
            self.driver.execute_script("arguments[0].click();", filters_btn)
        WebDriverWait(self.driver, 10).until(
            lambda d: len(self.get_shadow_root().find_elements(
                By.CSS_SELECTOR, "button, div"
            )) > 0
        )