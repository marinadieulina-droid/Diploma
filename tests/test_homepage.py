import allure

@allure.feature("Homepage")
@allure.story("Homepage Availability")
@allure.title("Verify homepage opens successfully")
def test_homepage(driver):

    with allure.step("Open homepage"):
        driver.get("https://www.ppl.cz")

    with allure.step("Verify page title"):
        assert "PPL" in driver.title