import allure
from pages.tracking_page import TrackingPage
from tests.test_data import (
    VALID_TRACKING_NUMBER,
    INVALID_TRACKING_NUMBER,
    INVALID_FORMAT_TRACKING_NUMBER,
    EXPECTED_ERROR_KEYWORD,
)
@allure.feature("Tracking")
@allure.story("Valid tracking number")
@allure.title("Verify shipment tracking history")
def test_shipment_details(driver):
    page = TrackingPage(driver)

    with allure.step("Open tracking page"):
        page.open()

    with allure.step("Accept cookies"):
        page.accept_cookies()

    with allure.step(f"Enter valid tracking number: {VALID_TRACKING_NUMBER}"):
        page.enter_tracking_number(VALID_TRACKING_NUMBER)

    with allure.step("Click search button"):
        page.click_search()

    with allure.step("Wait for tracking result"):
        page.wait_for_result()

    with allure.step("Get shipment history"):
        history = page.get_history()

    with allure.step("Verify shipment history is not empty"):
        assert len(history) > 0, (
            f"Tracking history is empty for number '{VALID_TRACKING_NUMBER}'. "
            "Expected at least one status record."
        )

    with allure.step("Verify each history record has date and status"):
        for idx, item in enumerate(history):
            assert item["date"], (
                f"Record #{idx} is missing a date. Full record: {item}"
            )
            assert item["status"], (
                f"Record #{idx} is missing a status. Full record: {item}"
            )


@allure.feature("Tracking")
@allure.story("Invalid tracking number")
@allure.title("Verify error message for non-existent tracking number")
def test_invalid_tracking_number(driver):
    page = TrackingPage(driver)

    with allure.step("Open tracking page"):
        page.open()

    with allure.step("Accept cookies"):
        page.accept_cookies()

    with allure.step(f"Enter invalid tracking number: {INVALID_TRACKING_NUMBER}"):
        page.enter_tracking_number(INVALID_TRACKING_NUMBER)

    with allure.step("Click search button"):
        page.click_search()

    with allure.step("Wait for tracking result"):
        page.wait_for_result()

    with allure.step("Verify error message is displayed"):
        error = page.get_error_message()
        assert error != "", (
            f"Expected an error message for invalid number '{INVALID_TRACKING_NUMBER}', "
            "but no message appeared."
        )

    with allure.step(f"Verify error message contains '{EXPECTED_ERROR_KEYWORD}'"):
        assert EXPECTED_ERROR_KEYWORD in error.lower(), (
            f"Expected error message to contain '{EXPECTED_ERROR_KEYWORD}', "
            f"but actual message is: '{error}'"
        )


@allure.feature("Tracking")
@allure.story("Letters and symbols")
@allure.title("Verify validation message for tracking number with letters and symbols")
def test_letters_and_symbols(driver):
    page = TrackingPage(driver)

    with allure.step("Open tracking page"):
        page.open()

    with allure.step("Accept cookies"):
        page.accept_cookies()

    with allure.step(f"Enter invalid format: '{INVALID_FORMAT_TRACKING_NUMBER}'"):
        page.enter_tracking_number(INVALID_FORMAT_TRACKING_NUMBER)

    with allure.step("Click search button"):
        page.click_search()

    with allure.step("Wait for validation result"):
        page.wait_for_result()

    with allure.step("Verify validation message is displayed"):
        error = page.get_error_message()
        assert error != "", (
            f"Expected a validation message for input '{INVALID_FORMAT_TRACKING_NUMBER}', "
            "but no message appeared."
        )