import allure
from pages.map_page import MapPage


@allure.feature("Map Features")
@allure.story("Filters and Geolocation")
@allure.title("Verify geolocation and map filters")
def test_map_features(driver):
    print("\n[INFO] Старт комплексного теста функционала карты.")

    # Инициализируем страницу карты и передаем ей driver
    map_page = MapPage(driver)

    with allure.step("Open pickup points map"):
        print("[INFO] Переход на страницу карты...")
        map_page.open()

    with allure.step("Accept cookies"):
        print("[INFO] Обработка cookie-баннеров...")
        map_page.accept_cookies()

    with allure.step("Verify and click geolocation button"):
        print("[INFO] Клик по кнопке определения геолокации...")
        map_page.click_geolocation_button()
        print("[SUCCESS] Кнопка геолокации успешно отработала.")

    with allure.step("Open filters panel"):
        print("[INFO] Открытие шторки фильтров...")
        map_page.open_filters_panel()

    with allure.step("Expand 'Typ místa' category if present"):
        print("[INFO] Раскрытие выпадающего блока 'Typ místa'...")
        map_page.expand_typ_mista_category()

    with allure.step("Select filters via standard elements"):
        print("[INFO] Поиск и выбор чекбоксов 'Shop' и 'Box'...")
        map_page.select_shop_and_box_filters()

    with allure.step("Apply filters"):
        print("[INFO] Применение выбранных фильтров...")
        map_page.apply_filters()

    with allure.step("Verify filtration flow completed"):
        print("[SUCCESS] Сценарий фильтрации карты успешно завершен по POM!")