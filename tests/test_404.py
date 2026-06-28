import allure
from pages.error_page import ErrorPage
from test_data import EXPECTED_404_TITLE


@allure.feature("Error Handling")
@allure.story("404 Page")
@allure.title("Verify 404 page is displayed")
def test_404_page(driver):
    page = ErrorPage(driver)

    with allure.step("Open invalid URL"):
        page.open_invalid_page()

    with allure.step("Verify 404 page title"):
        actual_title = page.get_title()
        assert EXPECTED_404_TITLE in actual_title, (
            f"Expected page title to contain '{EXPECTED_404_TITLE}', "
            f"but got '{actual_title}'."
        )