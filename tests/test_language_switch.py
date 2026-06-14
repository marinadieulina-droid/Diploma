import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Localization")
@allure.story("Language Switch")
@allure.title("Verify language selector works")
def test_language_switch(driver):

    with allure.step("Open homepage"):
        driver.get("https://www.ppl.cz")

    with allure.step("Accept cookies"):
        cookie_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "onetrust-accept-btn-handler")
            )
        )
        cookie_btn.click()

    with allure.step("Find language selector"):
        language = Select(
            driver.find_element(
                By.CSS_SELECTOR,
                ".language-selector-select"
            )
        )

    with allure.step("Verify current language"):
        selected_language = (
            language.first_selected_option.text.lower()
        )

        print("Current language:", selected_language)

        assert selected_language in ["cs", "en"]