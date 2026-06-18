import allure
import pytest
from pages.tracking_page import TrackingPage

@allure.feature("Tracking")
@allure.story("Valid tracking number")
@allure.title("Verify shipment tracking history")
def test_shipment_details(driver):
    page = TrackingPage(driver)
    with allure.step("Open tracking page"):
        page.open()

    with allure.step("Accept cookies"):
        page.accept_cookies()

    tracking_number = "20157771913"

    with allure.step("Enter valid tracking number"):
        print(
            f"\nВводим валидный номер отправления: "
            f"{tracking_number}"
        )
        page.enter_tracking_number(tracking_number)

    with allure.step("Click search button"):
        page.click_search()

    with allure.step("Wait for tracking result"):
        page.wait_for_result()

    with allure.step("Get shipment history"):
        history = page.get_history()

        print(
            "\n========== Получаем статус посылки ==========\n"
        )

        for item in history:
            print(f"DATE: {item['date']}")
            print(f"STATUS: {item['status']}")
            print("-" * 50)

    with allure.step("Verify shipment history is not empty"):
        assert len(history) > 0, \
            "История отслеживания пуста!"

@allure.feature("Tracking")
@allure.story("Invalid tracking number")
@allure.title("Verify invalid tracking number")
def test_invalid_tracking_number(driver):
    page = TrackingPage(driver)
    with allure.step("Open tracking page"):
        page.open()

    with allure.step("Accept cookies"):
        page.accept_cookies()

    tracking_number = "000000000000"

    with allure.step("Enter invalid tracking number"):
        print(
            f"\nВводим номер отправления: "
            f"{tracking_number}"
        )
        page.enter_tracking_number(tracking_number)

    with allure.step("Click search button"):
        page.click_search()

    with allure.step("Wait for tracking result"):
        page.wait_for_result()

    with allure.step("Get error message"):
        error = page.get_error_message()
        print(f"\nСообщение об ошибке: {error}")

    with allure.step("Verify shipment not found message"):
        assert error != "", \
            "Сообщение об ошибке не появилось!"

        assert "nenalezena" in error.lower(), \
            f"Ожидалось 'nenalezena', но получено: {error}"

@allure.feature("Tracking")
@allure.story("Letters and symbols")
@allure.title("Verify tracking search with letters and symbols")
def test_letters_and_symbols(driver):
    page = TrackingPage(driver)
    with allure.step("Open tracking page"):
        page.open()

    with allure.step("Accept cookies"):
        page.accept_cookies()

    tracking_number = "ABC123!!!"

    with allure.step("Enter letters and symbols"):
        print(
            f"\nВводим номер отправления: "
            f"{tracking_number}"
        )
        page.enter_tracking_number(tracking_number)

    with allure.step("Click search button"):
        page.click_search()

    with allure.step("Wait for validation result"):
        page.wait_for_result()

    with allure.step("Get validation message"):
        error = page.get_error_message()
        print(f"\nСообщение об ошибке: {error}")

    with allure.step("Verify validation message exists"):
        assert error != "", \
            "Сообщение об ошибке или валидации не появилось для неверного формата!"