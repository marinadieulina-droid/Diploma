import allure

from pages.homepage_page import HomepagePage


@allure.feature("Accessibility")
@allure.story("Keyboard Navigation")
@allure.title("Verify keyboard navigation using TAB key")
def test_keyboard_navigation(driver):
    """
    Проверка поддержки клавиатурной навигации на сайте.
    """

    print("\n=== START TEST: KEYBOARD NAVIGATION ===")

    # Создание объекта страницы
    homepage = HomepagePage(driver)

    with allure.step("Open homepage"):
        print("[STEP 1] Opening homepage...")
        homepage.open()
        print("[PASS] Homepage opened successfully.")

    with allure.step("Accept cookies"):
        print("[STEP 2] Accepting cookies...")
        homepage.accept_cookies()
        print("[PASS] Cookies accepted.")

    with allure.step("Navigate using TAB key"):
        print("[STEP 3] Navigating through page using TAB key...")

        # Выполняем 5 нажатий TAB
        active_element = homepage.navigate_with_tab(5)

        print("[PASS] TAB navigation completed.")

    with allure.step("Check active element"):
        print("[STEP 4] Checking active element...")

        tag_name = active_element.tag_name
        element_text = active_element.text.strip()

        print(f"[INFO] Active element tag: {tag_name}")

        if element_text:
            print(f"[INFO] Active element text: {element_text}")

        allure.attach(
            f"Tag: {tag_name}\nText: {element_text}",
            name="Active Element",
            attachment_type=allure.attachment_type.TEXT
        )

        assert active_element is not None, (
            "No active element found after keyboard navigation."
        )

        print("[PASS] Active element found.")

    with allure.step("Verify element is enabled"):
        print("[STEP 5] Verifying active element is enabled...")

        assert active_element.is_enabled(), (
            "Active element is disabled."
        )

        print("[PASS] Active element is enabled.")

    print("=== TEST PASSED: KEYBOARD NAVIGATION ===\n")