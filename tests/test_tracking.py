import allure

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Shipment Tracking")
@allure.story("Tracking Number Input")
@allure.title("Verify tracking number can be entered")
def test_tracking_input(driver):

    with allure.step("Open tracking page"):
        driver.get("https://www.ppl.cz/vyhledavani")

    with allure.step("Enter tracking number"):
        search_field = driver.find_element(
            By.NAME,
            "q"
        )

        search_field.send_keys("123456789")

    with allure.step("Verify entered value"):
        entered_value = search_field.get_attribute("value")

        print("Entered value:", entered_value)

        assert entered_value == "123456789"


@allure.feature("Shipment Tracking")
@allure.story("Search Function")
@allure.title("Verify search button works")
def test_search_button(driver):

    with allure.step("Open tracking page"):
        driver.get("https://www.ppl.cz/vyhledavani")

    with allure.step("Accept cookies"):
        cookie_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "onetrust-accept-btn-handler")
            )
        )
        cookie_btn.click()

    with allure.step("Enter tracking number"):
        search_field = driver.find_element(
            By.NAME,
            "q"
        )

        search_field.send_keys("123456789")

    with allure.step("Click search button"):
        search_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Odeslat"]')
            )
        )

        search_btn.click()

    with allure.step("Verify search executed"):
        print("Current URL:", driver.current_url)

        assert "vyhledavani" in driver.current_url


@allure.feature("Shipment Tracking")
@allure.story("Invalid Tracking Number")
@allure.title("Verify non-existing tracking number")
def test_invalid_tracking_number(driver):

    invalid_number = "000000000000000000"

    with allure.step("Open tracking page"):
        driver.get("https://www.ppl.cz/vyhledavani")

    with allure.step("Accept cookies"):
        cookie_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "onetrust-accept-btn-handler")
            )
        )
        cookie_btn.click()

    with allure.step("Enter invalid tracking number"):
        search_field = driver.find_element(
            By.NAME,
            "q"
        )

        search_field.send_keys(invalid_number)

    with allure.step("Click search button"):
        search_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Odeslat"]')
            )
        )

        search_btn.click()

    with allure.step("Verify error message"):
        error_message = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(text(),'Nebyly nalezeny žádné produkty')]"
                )
            )
        )

        print("Tracking number:", invalid_number)
        print("Result:", error_message.text)

        assert "Nebyly nalezeny žádné produkty" in error_message.text


@allure.feature("Shipment Tracking")
@allure.story("Invalid Tracking Number Format")
@allure.title("Verify invalid tracking number format")
def test_invalid_format_tracking_number(driver):

    invalid_number = "ABC123!!!"

    with allure.step("Open tracking page"):
        driver.get("https://www.ppl.cz/vyhledavani")

    with allure.step("Accept cookies"):
        cookie_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "onetrust-accept-btn-handler")
            )
        )
        cookie_btn.click()

    with allure.step("Enter invalid format"):
        search_field = driver.find_element(
            By.NAME,
            "q"
        )

        search_field.send_keys(invalid_number)

    with allure.step("Click search button"):
        search_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button[aria-label="Odeslat"]')
            )
        )

        search_btn.click()

    with allure.step("Verify error message"):
        error_message = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(text(),'Nebyly nalezeny žádné produkty')]"
                )
            )
        )

        print("Tracking number:", invalid_number)
        print("Result:", error_message.text)

        assert "Nebyly nalezeny žádné produkty" in error_message.text