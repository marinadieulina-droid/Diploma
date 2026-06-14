import allure

@allure.feature("Error Handling")
@allure.story("404 Page")
@allure.title("Verify 404 page is displayed")
def test_404_page(driver):

    with allure.step("Open invalid URL"):
        driver.get(
            "https://www.ppl.cz/non-existing-page"
        )

    with allure.step("Verify page response"):
        assert driver.current_url