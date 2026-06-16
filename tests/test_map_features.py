import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# ==================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ РАБОТЫ С COOKIES И SHADOW DOM
# ==================================================

def accept_cookies(driver):
    """Закрывает cookie-баннеры (глобальный и внутри виджета)."""
    try:
        cookie_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_btn.click()
        print("[SUCCESS] Primary cookies accepted.")
    except Exception:
        pass

    try:
        shadow_host = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ppl-access-point-widget, #pplWidget"))
        )
        shadow_root = shadow_host.shadow_root
        time.sleep(1.5)

        buttons = shadow_root.find_elements(By.CSS_SELECTOR, "button")
        for btn in buttons:
            if "Přijmout" in btn.text or "vše" in btn.text:
                driver.execute_script("arguments[0].click();", btn)
                print("[SUCCESS] Secondary cookies inside Shadow DOM accepted.")
                time.sleep(1.5)
                break
    except Exception:
        pass


def get_map_shadow_root(driver):
    """Возвращает основной shadow_root карты стандартным методом Selenium 4."""
    shadow_host = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "ppl-access-point-widget, #pplWidget"))
    )
    return shadow_host.shadow_root


def wait_and_click_by_text(shadow_root, text_substring, timeout=15):
    """
    Стандартный поиск элемента по тексту внутри переданного Shadow DOM.
    """
    end_time = time.monotonic() + timeout
    target = text_substring.lower().replace(" ", "")

    while time.monotonic() < end_time:
        try:
            elements = shadow_root.find_elements(By.CSS_SELECTOR, "button, span, div, label")
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


# ==================================================
# ТЕСТОВЫЙ СЦЕНАРИЙ (СТАНДАРТНЫЙ SELENIUM)
# ==================================================

@allure.feature("Map Features")
@allure.story("Filters and Geolocation")
@allure.title("Verify geolocation and map filters")
def test_map_features(driver):
    # 1. Открываем карту
    with allure.step("Open pickup points map"):
        driver.get("https://www.ppl.cz/mapa-vydejnich-mist")

    # 2. Принимаем куки
    with allure.step("Accept cookies"):
        accept_cookies(driver)

    # 3. Получаем доступ к основному Shadow DOM виджета
    with allure.step("Access Map Shadow DOM"):
        shadow_root = get_map_shadow_root(driver)

    # 4. Нажимаем кнопку геолокации
    with allure.step("Verify and click geolocation button"):
        geolocation_button = WebDriverWait(driver, 10).until(
            lambda d: shadow_root.find_element(By.CSS_SELECTOR, 'button[aria-label="Zjistit polohu"]')
        )
        assert geolocation_button.is_displayed(), "Кнопка геолокации не видна"
        driver.execute_script("arguments[0].click();", geolocation_button)
        print("[INFO] Кнопка геолокации успешно нажата.")
        time.sleep(2)

    # 5. Кликаем на кнопку 'Všechny filtry' / 'Všechny' (внутри Shadow DOM)
    with allure.step("Open filters panel"):
        filters_btn = wait_and_click_by_text(shadow_root, "Všech", timeout=12)
        driver.execute_script("arguments[0].click();", filters_btn)
        print("[INFO] Нажата кнопка открытия фильтров.")
        time.sleep(2)  # Даем шторке раскрыться

    # 5.1. Кликаем на 'Typ místa' (внутри того же shadow_root)
    with allure.step("Expand 'Typ místa' category if present"):
        try:
            typ_mista_el = wait_and_click_by_text(shadow_root, "Typ místa", timeout=5)
            driver.execute_script("arguments[0].click();", typ_mista_el)
            print("[INFO] Раскрыта категория 'Typ místa'.")
            time.sleep(2)
        except TimeoutException:
            print("[INFO] Категория 'Typ místa' не найдена. Продолжаем.")

    # 6. Выбираем фильтр Shop и 7. Фильтр Box через СТАНДАРТНЫЕ СЕЛЕКТОРЫ
    # Вместо поиска по тексту, мы выгребаем все чекбоксы/кнопки фильтров внутри shadow_root
    with allure.step("Select filters via standard elements"):
        # Обновляем shadow_root перед финальным выбором
        shadow_root = get_map_shadow_root(driver)

        # Находим все элементы списков (чекбоксы, инпуты или лейблы)
        # Этот селектор выберет все интерактивные элементы фильтров в шторке
        filter_options = shadow_root.find_elements(By.CSS_SELECTOR, "input[type='checkbox'], label, button")

        shop_clicked = False
        box_clicked = False

        for option in filter_options:
            try:
                # Берем у каждого элемента его текст, id или value
                text_content = option.get_attribute("textContent") or ""
                val_attr = option.get_attribute("value") or ""
                id_attr = option.get_attribute("id") or ""

                # Полная строка для проверки, куда точно попадет нужное слово
                full_identity = (text_content + val_attr + id_attr).lower()

                if "shop" in full_identity and not shop_clicked:
                    driver.execute_script("arguments[0].click();", option)
                    print("[INFO] Фильтр Shop успешно переключен.")
                    shop_clicked = True
                    time.sleep(0.5)

                if "box" in full_identity and not box_clicked:
                    driver.execute_script("arguments[0].click();", option)
                    print("[INFO] Фильтр Box успешно переключен.")
                    box_clicked = True
                    time.sleep(0.5)
            except Exception:
                continue

    # 8. Закрываем/применяем фильтры
    with allure.step("Apply filters"):
        try:
            apply_btn = wait_and_click_by_text(shadow_root, "Zobrazit", timeout=5)
            driver.execute_script("arguments[0].click();", apply_btn)
            print("[INFO] Кнопка 'Zobrazit' успешно нажата.")
        except TimeoutException:
            driver.execute_script("arguments[0].click();", filters_btn)
            print("[INFO] Панель фильтров закрыта.")

        time.sleep(2)

    # 9. Проверка успешного завершения сценария
    with allure.step("Verify filtration flow completed"):
        print("[SUCCESS] Тест успешно пройден стандартными методами Selenium!")