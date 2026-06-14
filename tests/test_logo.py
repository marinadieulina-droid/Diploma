import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Homepage")
@allure.story("Logo")
@allure.title("Verify company logo is displayed")
def test_logo(driver):

    with allure.step("Open homepage"):
        driver.get("https://www.ppl.cz")

    with allure.step("Accept cookies"):
        cookie_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "onetrust-accept-btn-handler")
            )
        )
        cookie_btn.click()

    with allure.step("Locate logo"):
        logo = driver.find_element(
            By.CSS_SELECTOR,
            ".header__logo"
        )

    with allure.step("Verify logo visibility"):
        assert logo.is_displayed()
    print("Logo is displayed successfully")