import allure
import pytest
from pages.tracking_page import TrackingPage

@allure.feature("Tracking")
@allure.story("Valid tracking number")
@allure.title("Verify shipment tracking history")
def test_shipment_details(driver):
    page = TrackingPage(driver)
    page.open()
    page.accept_cookies()

    tracking_number = "20157771913"
    print(f"\nВводим валидный номер отправления: {tracking_number}")

    page.enter_tracking_number(tracking_number)
    page.click_search()
    page.wait_for_result()

    history = page.get_history()
    print("\n========== Получаем статус посылки ==========\n")
    for item in history:
        print(f"DATE: {item['date']}")
        print(f"STATUS: {item['status']}")
        print("-" * 50)

    assert len(history) > 0, "История отслеживания пуста!"

@allure.feature("Tracking")
@allure.story("Invalid tracking number")
@allure.title("Verify invalid tracking number")
def test_invalid_tracking_number(driver):
    page = TrackingPage(driver)
    page.open()
    page.accept_cookies()

    tracking_number = "000000000000"
    print(f"\nВВодим номер отправления: {tracking_number}")

    page.enter_tracking_number(tracking_number)
    page.click_search()
    page.wait_for_result()

    error = page.get_error_message()
    print(f"\nСообщение об ошибке: {error}")

    assert error != "", "Сообщение об ошибке не появилось!"
    assert "nenalezena" in error.lower(), f"Ожидалось 'nenalezena', но получено: {error}"

@allure.feature("Tracking")
@allure.story("Letters and symbols")
@allure.title("Verify tracking search with letters and symbols")
def test_letters_and_symbols(driver):
    page = TrackingPage(driver)
    page.open()
    page.accept_cookies()

    tracking_number = "ABC123!!!"
    print(f"\nВВодим номер отправления: {tracking_number}")

    page.enter_tracking_number(tracking_number)
    page.click_search()
    page.wait_for_result()

    error = page.get_error_message()
    print(f"\nСообщение об ошибке: {error}")

    # Проверка, что сообщение об ошибке вообще появилось
    assert error != "", "Сообщение об ошибке или валидации не появилось для неверного формата!"