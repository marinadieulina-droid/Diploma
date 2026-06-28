import allure
from selenium.webdriver.support.ui import WebDriverWait
from pages.homepage_page import HomepagePage
from selenium.webdriver.support.ui import Select


@allure.feature("Localization")
@allure.story("Language Switch")
@allure.title("Verify language switching works")
def test_language_switch(driver):
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        page.open()

    with allure.step("Accept cookies"):
        page.accept_cookies()

    with allure.step("Get current language"):
        current_language = page.get_selected_language()
        allowed_languages = ["cs", "en"]
        assert current_language in allowed_languages, (
            f"Expected one of {allowed_languages}, "
            f"but got '{current_language}'."
        )

    with allure.step("Switch language"):
        if current_language == "cs":
            page.switch_language("en")
            expected_language = "en"
            expected_url_part = "/en/"
        else:
            page.switch_language("cs")
            expected_language = "cs"
            expected_url_part = "ppl.cz"

        # Ждём пока язык в селекторе реально изменится
        WebDriverWait(driver, 10).until(
            lambda d: page.get_selected_language() == expected_language
        )

    with allure.step("Verify language changed"):
        new_language = page.get_selected_language()
        assert new_language == expected_language, (
            f"Expected language '{expected_language}', "
            f"but got '{new_language}'."
        )

    with allure.step("Verify page title"):
        page_title = driver.title
        assert page_title.strip() != "", (
            "Page title is empty after language switch."
        )

