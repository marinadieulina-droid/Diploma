import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ==================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==================================================

def accept_cookies(driver):
    """Закрывает окно cookies, если оно отображается на экране."""
    try:
        print("[INFO] Checking for cookie banner...")
        cookie_btn = WebDriverWait(driver, 7).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        cookie_btn.click()
        print("[SUCCESS] Cookies accepted successfully.")
    except Exception:
        print("[INFO] Cookie banner did not appear or is not interactable.")


def open_valid_shipment(driver):
    """Открывает страницу трекинга и вводит корректный номер посылки."""
    with allure.step("Open tracking page and submit valid shipment ID"):
        print("[INFO] Navigating to tracking page...")
        driver.get("https://www.ppl.cz/vyhledat-zasilku")

        accept_cookies(driver)

        print("[INFO] Waiting for tracking input field...")
        tracking_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "shipmentId"))
        )
        tracking_field.clear()
        tracking_field.send_keys("20157771913")
        print("[INFO] Valid shipment ID '20157771913' entered.")

        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        driver.execute_script("arguments[0].click();", search_button)
        print("[INFO] Search form submitted via JS click.")

        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(),'Stav vaší zásilky')]"))
        )
        print("[SUCCESS] Page with shipment status loaded successfully.")


# ==================================================
# ТЕСТ 1: Проверка ввода номера отслеживания
# ==================================================
@allure.feature("Real Shipment Tracking")
@allure.story("Tracking Number Input")
@allure.title("Verify tracking number can be entered into the field")
@allure.severity(allure.severity_level.NORMAL)
def test_tracking_input(driver):
    tracking_number = "20157771913"

    with allure.step("Open shipment tracking page"):
        print("[START] test_tracking_input")
        driver.get("https://www.ppl.cz/vyhledat-zasilku")
        print("[INFO] Tracking page loaded.")

    accept_cookies(driver)

    with allure.step("Enter tracking number and verify value"):
        tracking_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "shipmentId"))
        )
        tracking_field.clear()
        tracking_field.send_keys(tracking_number)

        entered_value = tracking_field.get_attribute("value")
        print(f"[DATA] Expected: {tracking_number} | Actual entered: {entered_value}")

        assert entered_value == tracking_number
        print("[SUCCESS] test_tracking_input passed.")


# ==================================================
# ТЕСТ 2: Проверка существующей посылки
# ==================================================
@allure.feature("Real Shipment Tracking")
@allure.story("Valid Tracking Number")
@allure.title("Verify existing shipment can be tracked successfully")
@allure.severity(allure.severity_level.CRITICAL)
def test_valid_tracking_number(driver):
    tracking_number = "20157771913"

    with allure.step("Open shipment tracking page"):
        print("[START] test_valid_tracking_number")
        driver.get("https://www.ppl.cz/vyhledat-zasilku")

    accept_cookies(driver)

    with allure.step("Enter valid tracking number"):
        tracking_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "shipmentId"))
        )
        tracking_field.clear()
        tracking_field.send_keys(tracking_number)
        print(f"[INFO] Tracking number '{tracking_number}' populated.")

    with allure.step("Click search button"):
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        driver.execute_script("arguments[0].click();", search_button)
        print("[INFO] Search button triggered.")

    with allure.step("Verify shipment information heading"):
        shipment_title = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(),'Stav vaší zásilky')]"))
        )
        print(f"[DATA] Header text found: '{shipment_title.text}'")
        print(f"[DATA] Current landing URL: {driver.current_url}")

        assert "Stav vaší zásilky" in shipment_title.text
        print("[SUCCESS] test_valid_tracking_number passed.")


# ==================================================
# ТЕСТ 3: Детали и статус посылки (Исправленный)
# ==================================================
# ТЕСТ 3: Детали и статус посылки (Исправленный)
# ==================================================
@allure.feature("Shipment Details")
@allure.story("Shipment Information Accordions")
@allure.title("Verify shipment detailed info and status table columns")
@allure.severity(allure.severity_level.NORMAL)
def test_shipment_details(driver):
    print("[START] test_shipment_details")
    open_valid_shipment(driver)

    # Шаг 1: Раскрытие аккордеона деталей. Используем точный тег label и normalize-space
    with allure.step("Expand 'Detail zásilky' accordion"):
        detail_accordion = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(normalize-space(), 'Detail zásilky')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", detail_accordion)
        driver.execute_script("arguments[0].click();", detail_accordion)
        print("[INFO] 'Detail zásilky' accordion expanded via JS.")

    with allure.step("Verify main shipment blocks (Sender, Reference, Weight)"):
        sender = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(), 'Odesílatel')]"))
        )
        reference = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(), 'Referenční číslo')]"))
        )
        weight = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(), 'Váha')]"))
        )

        print("[SUCCESS] Elements 'Odesílatel', 'Referenční číslo', 'Váha' are visible.")

    # Шаг 2: Раскрытие аккордеона таблицы статусов
    with allure.step("Expand 'Detail stavu zásilky' accordion"):
        status_accordion = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//label[contains(normalize-space(), 'Detail stavu zásilky')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", status_accordion)
        driver.execute_script("arguments[0].click();", status_accordion)
        print("[INFO] 'Detail stavu zásilky' accordion expanded via JS.")

    with allure.step("Verify status table headers visibility"):
        date_column = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(), 'Datum a čas')]"))
        )
        status_column = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(normalize-space(), 'Stav zásilky')]"))
        )

        print("[SUCCESS] Status table elements 'Datum a čas' and 'Stav zásilky' are visible.")
        print("[SUCCESS] test_shipment_details passed.")


# ==================================================
# ТЕСТ 4: Проверка несуществующей посылки
# ==================================================
@allure.feature("Real Shipment Tracking")
@allure.story("Invalid Tracking Number")
@allure.title("Verify error message for non-existing shipment ID")
@allure.severity(allure.severity_level.NORMAL)
def test_invalid_tracking_number(driver):
    invalid_number = "0000000000"

    with allure.step("Open shipment tracking page"):
        print("[START] test_invalid_tracking_number")
        driver.get("https://www.ppl.cz/vyhledat-zasilku")

    accept_cookies(driver)

    with allure.step("Enter non-existing tracking number"):
        tracking_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "shipmentId"))
        )
        tracking_field.clear()
        tracking_field.send_keys(invalid_number)
        print(f"[INFO] Invalid ID '{invalid_number}' entered.")

    with allure.step("Click search button"):
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        driver.execute_script("arguments[0].click();", search_button)

    with allure.step("Verify 'Zásilka nenalezena' error message text"):
        error_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Zásilka nenalezena')]"))
        )

        print(f"[DATA] Extracted error message text: '{error_message.text}'")
        assert "Zásilka nenalezena" in error_message.text
        print("[SUCCESS] test_invalid_tracking_number passed.")


# ==================================================
# ТЕСТ 5: Проверка неверного формата номера
# ==================================================
@allure.feature("Real Shipment Tracking")
@allure.story("Invalid Tracking Number Format")
@allure.title("Verify inline validation message for invalid chars format")
@allure.severity(allure.severity_level.NORMAL)
def test_invalid_format_tracking_number(driver):
    invalid_number = "ABC123!!!"

    with allure.step("Open shipment tracking page"):
        print("[START] test_invalid_format_tracking_number")
        driver.get("https://www.ppl.cz/vyhledat-zasilku")

    accept_cookies(driver)

    with allure.step("Enter tracking ID with invalid characters format"):
        tracking_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "shipmentId"))
        )
        tracking_field.clear()
        tracking_field.send_keys(invalid_number)
        print(f"[INFO] Value with wrong format '{invalid_number}' typed.")

    with allure.step("Verify inline red validation alert message"):
        validation_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span.c-help-block"))
        )

        print(f"[DATA] Extracted validation tip: '{validation_message.text}'")
        # Учтена полная строка ошибки из лога ("Povoleny jsou pouze číslice a velká a malá písmena")
        assert "Povoleny jsou pouze číslice" in validation_message.text
        print("[SUCCESS] test_invalid_format_tracking_number passed.")