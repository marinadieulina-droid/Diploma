import allure
from pages.homepage_page import HomepagePage


@allure.feature("Meta Tags")
@allure.story("Page Title")
@allure.title("Verify page title")
def test_page_title(driver):
    print("\n[INFO] Старт теста: Проверка заголовка страницы.")
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        page.open()

    with allure.step("Verify page title text"):
        title = page.get_title()
        print(f"[INFO] Получен заголовок: '{title}'")

        assert title != "", "Заголовок страницы пустой"
        assert "PPL" in title, f"Ожидали увидеть 'PPL' в заголовке, но получили '{title}'"
        print("[SUCCESS] Заголовок страницы успешно проверен.")


@allure.feature("Meta Tags")
@allure.story("Meta Description")
@allure.title("Verify meta description")
def test_meta_description(driver):
    print("\n[INFO] Старт теста: Проверка мета-описания страницы.")
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        page.open()

    with allure.step("Verify meta description content"):
        description = page.get_meta_description()
        print(f"[INFO] Получено описание (Description): '{description}'")

        assert description != "", "Мета-описание страницы пустое"
        print("[SUCCESS] Мета-описание успешно проверено.")


@allure.feature("Meta Tags")
@allure.story("Open Graph")
@allure.title("Verify Open Graph title")
def test_og_title(driver):
    print("\n[INFO] Старт теста: Проверка Open Graph заголовка (og:title).")
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        page.open()

    with allure.step("Verify og:title content"):
        title = page.get_og_title()
        print(f"[INFO] Получен Open Graph Title: '{title}'")

        assert title != "", "Тег og:title пустой"
        print("[SUCCESS] Тег og:title успешно проверен.")


@allure.feature("Meta Tags")
@allure.story("Open Graph")
@allure.title("Verify Open Graph description")
def test_og_description(driver):
    print("\n[INFO] Старт теста: Проверка Open Graph описания (og:description).")
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        page.open()

    with allure.step("Verify og:description content"):
        description = page.get_og_description()
        print(f"[INFO] Получен Open Graph Description: '{description}'")

        assert description != "", "Тег og:description пустой"
        print("[SUCCESS] Тег og:description успешно проверен.")


@allure.feature("Meta Tags")
@allure.story("Open Graph")
@allure.title("Verify Open Graph URL")
def test_og_url(driver):
    print("\n[INFO] Старт теста: Проверка Open Graph URL (og:url).")
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        page.open()

    with allure.step("Verify og:url content"):
        url = page.get_og_url()
        print(f"[INFO] Получен Open Graph URL: '{url}'")

        assert url != "", "Тег og:url пустой"
        print("[SUCCESS] Тег og:url успешно проверен.")