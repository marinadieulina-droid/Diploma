import allure
from pages.homepage_page import HomepagePage


@allure.feature("Navigation")
@allure.story("Main Menu")
@allure.title("Verify navigation menu and links")
def test_navigation_links(driver):
    print("\n[INFO] Старт теста: Проверка главного навигационного меню сайта.")
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        print("[INFO] Открываем главную страницу...")
        page.open()

    with allure.step("Accept cookies"):
        print("[INFO] Принимаем куки-файлы...")
        page.accept_cookies()

    with allure.step("Get navigation links"):
        print("[INFO] Извлекаем ссылки из пунктов меню...")
        menu_links = page.get_navigation_links()

        print(f"[INFO] Количество найденных пунктов меню: {len(menu_links)}")
        assert len(menu_links) >= 5, \
            f"Ожидали как минимум 5 пунктов меню, но нашли только {len(menu_links)}"

    with allure.step("Verify menu links validity"):
        print("[INFO] Начинаем валидацию URL-адресов...")
        for href in menu_links:
            print(f"[INFO] Проверка ссылки: '{href}'")

            assert href is not None, "Обнаружен пункт меню без атрибута 'href'"
            assert href.startswith("http"), \
                f"Ссылка '{href}' некорректна (должна начинаться с http/https)"

        print("[SUCCESS] Все ссылки меню успешно прошли проверку формата.")