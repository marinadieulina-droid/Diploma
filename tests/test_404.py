import allure
from pages.error_page import ErrorPage


@allure.feature("Error Handling")
@allure.story("404 Page")
@allure.title("Verify 404 page is displayed")
def test_404_page(driver):
    print("\n[INFO] Старт теста: Проверка обработки ошибки 404.")

    # Инициализируем страницу ошибки
    page = ErrorPage(driver)

    with allure.step("Open invalid URL"):
        print("[INFO] Открываем несуществующую страницу...")
        page.open_invalid_page()
        print("[SUCCESS] Браузер перешел по некорректному адресу.")

    with allure.step("Verify page title"):
        print("[INFO] Получаем заголовок страницы...")
        actual_title = page.get_title()

        # Заголовок страницы 404 на PPL обычно содержит "Stránka nenalezena" (Страница не найдена)
        expected_title_part = "Stránka nenalezena"

        print(f"[INFO] Ожидаем, что в заголовке '{actual_title}' есть текст '{expected_title_part}'")

        # Проверяем, что подстрока ошибки есть в заголовке вкладки
        assert expected_title_part in actual_title, \
            f"Ожидали ошибку 404, но открылась страница с заголовком: '{actual_title}'"

        print("[SUCCESS] Страница 404 успешно отображена, заголовок верный.")