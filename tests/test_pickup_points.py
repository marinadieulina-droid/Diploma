import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==================================================

def accept_cookies(driver):
    """Ожидает инициализацию виджета карты и закрывает куки внутри Shadow DOM."""
    # 1. Закрываем главное (первое) окно куки
    try:
        print("[INFO] Checking for primary cookie banner...")
        cookie_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_btn.click()
        print("[SUCCESS] Primary cookies accepted.")
    except Exception:
        print("[INFO] Primary cookie banner did not appear.")

    # 2. Ожидаем появление хост-элемента виджета карты
    try:
        print("[INFO] Waiting for map widget to mount in DOM...")
        shadow_host = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "ppl-access-point-widget, #pplWidget, div[class*='widget']"))
        )

        # Динамическое ожидание готовности shadow_root (пока он перестанет быть None)
        WebDriverWait(driver, 10).until(lambda d: shadow_host.shadow_root is not None)
        shadow_root = shadow_host.shadow_root
        print("[SUCCESS] Accessed Shadow DOM path successfully.")

        # Даем полсекунды на рендеринг внутренней верстки модального окна
        time.sleep(0.5)

        # Ищем кнопки внутри Shadow DOM
        buttons = shadow_root.find_elements(By.CSS_SELECTOR, "button")
        target_button = None
        for btn in buttons:
            if "Přijmout" in btn.text or "vše" in btn.text:
                target_button = btn
                break

        if target_button:
            # Кликаем через JS, чтобы обойти возможное перекрытие другими слоями
            driver.execute_script("arguments[0].click();", target_button)
            print("[SUCCESS] Secondary cookies inside Shadow DOM accepted.")
            # Даем анимации затемнения (overlay) полностью исчезнуть
            time.sleep(1.5)
        else:
            print("[INFO] Button 'Přijmout vše' not found inside Shadow DOM targets.")

    except Exception as e:
        print(f"[INFO] Shadow DOM cookie handler skipped or finished: {str(e)}")


def get_map_search_field(driver):
    """Находит инпут поиска, скрытый внутри Shadow DOM виджета карты."""
    print("[INFO] Fetching search input field from Shadow DOM...")
    try:
        shadow_host = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ppl-access-point-widget, #pplWidget"))
        )
        WebDriverWait(driver, 5).until(lambda d: shadow_host.shadow_root is not None)
        shadow_root = shadow_host.shadow_root

        search_field = shadow_root.find_element(By.CSS_SELECTOR, "input[type='text'], input.search-input")
        print("[SUCCESS] Map search field located inside Shadow DOM.")
        return search_field
    except Exception:
        print("[WARNING] Shadow DOM input search failed. Falling back to global DOM...")

    return WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Hledejte'], input.search-input"))
    )


# ==================================================
# ТЕСТ 1: Открытие страницы карты
# ==================================================
@allure.feature("Pickup Points Map")
@allure.story("Map Page Navigation")
@allure.title("Verify pickup points map page opens successfully")
@allure.severity(allure.severity_level.CRITICAL)
def test_pickup_points_page(driver):
    print("[START] test_pickup_points_page")

    with allure.step("Open pickup points map URL"):
        driver.get("https://www.ppl.cz/mapa-vydejnich-mist")
        print("[INFO] Navigation to map page completed.")

    with allure.step("Handle all cookie banners"):
        accept_cookies(driver)

    with allure.step("Verify current landing URL"):
        current_url = driver.current_url
        print(f"[DATA] Current URL: {current_url}")
        assert "mapa-vydejnich-mist" in current_url
        print("[SUCCESS] test_pickup_points_page passed.")


# ==================================================
# ТЕСТ 2: Отображение поля поиска
# ==================================================
@allure.feature("Pickup Points Map")
@allure.story("Search Field Verification")
@allure.title("Verify map search input field is displayed")
@allure.severity(allure.severity_level.NORMAL)
def test_search_field_displayed(driver):
    print("[START] test_search_field_displayed")

    with allure.step("Open pickup points map"):
        driver.get("https://www.ppl.cz/mapa-vydejnich-mist")

    with allure.step("Handle all cookie banners"):
        accept_cookies(driver)

    with allure.step("Locate map search field input"):
        search_field = get_map_search_field(driver)

    with allure.step("Verify search field visibility"):
        assert search_field is not None
        print("[SUCCESS] test_search_field_displayed passed.")


# ==================================================
# ТЕСТ 3: Поиск выездных мест по городу
# ==================================================
@allure.feature("Pickup Points Map")
@allure.story("Search By Criteria")
@allure.title("Verify interactive map search by city name")
@allure.severity(allure.severity_level.NORMAL)
def test_search_by_city(driver):
    print("[START] test_search_by_city")
    city = "Praha"

    with allure.step("Open pickup points map"):
        driver.get("https://www.ppl.cz/mapa-vydejnich-mist")

    with allure.step("Handle all cookie banners"):
        accept_cookies(driver)

    with allure.step("Locate map search field"):
        search_field = get_map_search_field(driver)

    with allure.step(f"Enter city name: {city}"):
        # Безопасный клик через JS, игнорирующий любые перекрывающие невидимые слои
        driver.execute_script("arguments[0].click();", search_field)
        driver.execute_script("arguments[0].value = '';", search_field)
        search_field.send_keys(city)
        print(f"[INFO] City value '{city}' sent to input field.")

    with allure.step("Verify entered city input value"):
        entered_value = search_field.get_attribute("value")
        print(f"[DATA] Expected: {city} | Actual value in field: {entered_value}")
        assert entered_value == city
        print("[SUCCESS] test_search_by_city passed.")


# ==================================================
# ТЕСТ 4: Поиск выездных мест по индексу (ZIP)
# ==================================================
@allure.feature("Pickup Points Map")
@allure.story("Search By Criteria")
@allure.title("Verify interactive map search by ZIP postal code")
@allure.severity(allure.severity_level.NORMAL)
def test_search_by_zip_code(driver):
    print("[START] test_search_by_zip_code")
    zip_code = "11000"

    with allure.step("Open pickup points map"):
        driver.get("https://www.ppl.cz/mapa-vydejnich-mist")

    with allure.step("Handle all cookie banners"):
        accept_cookies(driver)

    with allure.step("Locate map search field"):
        search_field = get_map_search_field(driver)

    with allure.step(f"Enter ZIP Code: {zip_code}"):
        # Безопасный клик через JS, игнорирующий любые перекрывающие невидимые слои
        driver.execute_script("arguments[0].click();", search_field)
        driver.execute_script("arguments[0].value = '';", search_field)
        search_field.send_keys(zip_code)
        print(f"[INFO] ZIP Code value '{zip_code}' sent to input field.")

    with allure.step("Verify entered ZIP code input value"):
        entered_value = search_field.get_attribute("value")
        print(f"[DATA] Expected: {zip_code} | Actual value in field: {entered_value}")
        assert entered_value == zip_code
        print("[SUCCESS] test_search_by_zip_code passed.")