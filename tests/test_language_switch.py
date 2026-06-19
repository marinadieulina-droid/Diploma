import allure
import time
from pages.homepage_page import HomepagePage

@allure.feature("Localization")
@allure.story("Language Switch")
@allure.title("Verify language switching works")
def test_language_switch(driver):
# Создаем объект главной страницы
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        print("[INFO] Открываем главную страницу...")
        page.open()
        print("[SUCCESS] Главная страница успешно загружена.")

    with allure.step("Accept cookies"):
        print("[INFO] Принимаем cookie-файлы...")
        page.accept_cookies()
        print("[SUCCESS] Cookie-файлы успешно приняты.")

    with allure.step("Get current language"):
        print("[INFO] Определяем текущий язык сайта...")

        current_language = page.get_selected_language()

        print(f"[INFO] Текущий язык: {current_language}")

    # Проверяем, что язык относится к поддерживаемым
        allowed_languages = ["cs", "en"]

        assert current_language in allowed_languages, (
            f"Ожидался один из языков {allowed_languages}, "
            f"но получено значение '{current_language}'"
        )

    with allure.step("Switch language"):
        print("[INFO] Выполняем переключение языка...")

    # Если сейчас чешский — переключаем на английский
        if current_language == "cs":
            page.switch_language("en")
            expected_language = "en"

    # Если сейчас английский — переключаем на чешский
        else:
            page.switch_language("cs")
            expected_language = "cs"

        time.sleep(3)

        print(f"[INFO] Ожидаемый язык после переключения: {expected_language}")

    with allure.step("Verify language changed"):
        print("[INFO] Проверяем результат переключения...")

        new_language = page.get_selected_language()

        assert new_language == expected_language, (
            f"Ожидался язык '{expected_language}', "
            f"но фактически получен '{new_language}'"
        )

        print(f"[SUCCESS] Язык успешно изменён на '{new_language}'.")

    with allure.step("Verify page title"):
        print("[INFO] Проверяем наличие заголовка страницы...")

        page_title = driver.title

        assert page_title.strip() != "", (
            "Заголовок страницы пустой после переключения языка."
        )

        print(f"[SUCCESS] Заголовок страницы: {page_title}")

    with allure.step("Verify current URL"):
        print("[INFO] Проверяем URL страницы...")

        current_url = driver.current_url

        assert current_url.startswith("https://"), (
            f"Некорректный URL: {current_url}"
        )

        print(f"[SUCCESS] Текущий URL: {current_url}")

    print("[SUCCESS] Тест переключения языка завершён успешно.")
