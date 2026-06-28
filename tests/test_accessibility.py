import allure
from pages.homepage_page import HomepagePage


@allure.feature("Accessibility")
@allure.story("Keyboard Navigation")
@allure.title("Verify keyboard navigation using TAB key")
def test_keyboard_navigation(driver):
    homepage = HomepagePage(driver)

    with allure.step("Open homepage"):
        homepage.open()

    with allure.step("Accept cookies"):
        homepage.accept_cookies()

    with allure.step("Navigate using TAB key"):
        # Количество нажатий TAB определено константой TAB_PRESSES_TO_TRACK_BUTTON
        # в классе HomepagePage — менять здесь не нужно
        active_element = homepage.navigate_with_tab()

    with allure.step("Verify active element is the Track shipment button"):
        tag_name = active_element.tag_name
        element_text = active_element.text.strip()

        allure.attach(
            f"Tag: {tag_name}\nText: {element_text}",
            name="Active Element",
            attachment_type=allure.attachment_type.TEXT
        )

        assert active_element.is_enabled()
        assert tag_name in ["a", "button", "input"]