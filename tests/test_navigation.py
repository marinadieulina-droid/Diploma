import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Navigation")
@allure.story("Main Menu")
@allure.title("Verify navigation menu and links")
def test_navigation_links(driver):

    with allure.step("Open homepage"):
        driver.get("https://www.ppl.cz/")

    with allure.step("Accept cookies"):
        cookie_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, "onetrust-accept-btn-handler")
            )
        )
        cookie_btn.click()

    with allure.step("Find menu items"):
        menu_items = driver.find_elements(
            By.CSS_SELECTOR,
            ".navbar__link"
        )

        print("Menu items found:", len(menu_items))

        assert len(menu_items) >= 5

    with allure.step("Verify menu links"):
        for item in menu_items:

            href = item.get_attribute("href")

            print("URL:", href)

            assert href is not None
            assert href.startswith("http")