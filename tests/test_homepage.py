import allure
from pages.homepage_page import HomepagePage


@allure.feature("Homepage")
@allure.story("Homepage Availability")
@allure.title("Verify homepage opens successfully")
def test_homepage(driver):
    print("\n[INFO] Старт теста: Проверка доступности главной страницы.")

    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        page.open()
        print("[SUCCESS] Главная страница успешно загружена.")

    with allure.step("Verify page title"):
        actual_title = page.get_title()
        expected_title = "Flexibilní doručení zásilek | Úvod | PPL CZ"

        assert actual_title == expected_title, f"Ожидали главную страницу, но получили '{actual_title}'"
        print("[SUCCESS] Проверка заголовка главной страницы успешно пройдена.")