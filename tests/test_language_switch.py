import allure
from pages.homepage_page import HomepagePage


@allure.feature("Localization")
@allure.story("Language Switch")
@allure.title("Verify language selector works")
def test_language_switch(driver):
    print("\n[INFO] Старт теста: Проверка локализации и селектора языков.")

    # Создаем объект страницы
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        print("[INFO] Открываем главную страницу...")
        page.open()
        print("[SUCCESS] Главная страница загружена.")

    with allure.step("Accept cookies"):
        print("[INFO] Ожидаем появления и принимаем куки...")
        page.accept_cookies()
        print("[SUCCESS] Куки успешно приняты.")

    with allure.step("Verify current language"):
        print("[INFO] Считываем текущий выбранный язык из селектора...")
        selected_language = page.get_selected_language()

        print(f"[INFO] Фактический выбранный язык на сайте: '{selected_language}'")

        #  ассерт с понятным сообщением на случай падения
        allowed_languages = ["cs", "en"]
        assert selected_language in allowed_languages, \
            f"Ожидали язык из списка {allowed_languages}, но получили '{selected_language}'"

        print(f"[SUCCESS] Проверка пройдена! Язык '{selected_language}' входит в список разрешенных.")