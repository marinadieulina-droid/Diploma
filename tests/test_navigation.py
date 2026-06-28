import allure
from pages.homepage_page import HomepagePage


@allure.feature("Navigation")
@allure.story("Main Menu")
@allure.title("Verify navigation menu and links")
def test_navigation_links(driver):
    page = HomepagePage(driver)

    # Минимальное количество пунктов меню определено на основе
    # анализа структуры навигации сайта PPL.cz:
    # О нас, Zásilky, Služby, Kariéra, Zákaznický servis — итого 5 пунктов.
    # При изменении структуры меню это значение нужно пересмотреть.
    MIN_MENU_ITEMS = 5

    with allure.step("Open homepage"):
        page.open()

    with allure.step("Accept cookies"):
        page.accept_cookies()

    with allure.step("Get navigation links"):
        menu_links = page.get_navigation_links()
        assert len(menu_links) >= MIN_MENU_ITEMS, (
            f"Expected at least {MIN_MENU_ITEMS} menu items, "
            f"but found only {len(menu_links)}."
        )

    with allure.step("Verify menu links validity"):
        for href in menu_links:
            assert href is not None, (
                "Found a menu item without an 'href' attribute."
            )
            assert href.startswith("https://"), (
                f"Expected link to start with 'https://', "
                f"but got '{href}'."
            )
            assert "ppl" in href, (
                f"Expected menu link to contain 'ppl', but got '{href}'."
            )