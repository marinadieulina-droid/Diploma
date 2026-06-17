import allure
from pages.map_page import MapPage

@allure.feature("Pickup Points Map")
@allure.story("Map Page Navigation")
@allure.title("Verify pickup points map page opens successfully")
@allure.severity(allure.severity_level.CRITICAL)
def test_pickup_points_page(driver):
    print("\n[START] test_pickup_points_page")
    map_page = MapPage(driver)

    with allure.step("Open pickup points map URL"):
        map_page.open()

    with allure.step("Handle all cookie banners"):
        map_page.accept_cookies()

    with allure.step("Verify current landing URL"):
        current_url = map_page.get_current_url()
        print(f"[DATA] Current URL: {current_url}")
        assert "mapa-vydejnich-mist" in current_url
        print("[SUCCESS] Страница карты успешно открыта.")


@allure.feature("Pickup Points Map")
@allure.story("Search Field Verification")
@allure.title("Verify map search input field is displayed")
@allure.severity(allure.severity_level.NORMAL)
def test_search_field_displayed(driver):
    print("\n[START] test_search_field_displayed")
    map_page = MapPage(driver)

    with allure.step("Open pickup points map"):
        map_page.open()

    with allure.step("Handle all cookie banners"):
        map_page.accept_cookies()

    with allure.step("Locate map search field input"):
        search_field = map_page.get_search_field()

    with allure.step("Verify search field visibility"):
        assert search_field is not None, "Поле поиска карты не найдено"
        print("[SUCCESS] Поле поиска отображается на карте.")


@allure.feature("Pickup Points Map")
@allure.story("Search By Criteria")
@allure.title("Verify interactive map search by city name")
@allure.severity(allure.severity_level.NORMAL)
def test_search_by_city(driver):
    print("\n[START] test_search_by_city")
    city = "Praha"
    map_page = MapPage(driver)

    with allure.step("Open pickup points map"):
        map_page.open()

    with allure.step("Handle all cookie banners"):
        map_page.accept_cookies()

    with allure.step(f"Enter city name: {city}"):
        map_page.enter_search_query(city)
        print(f"[INFO] Значение города '{city}' отправлено в поле поиска.")

    with allure.step("Verify entered city input value"):
        entered_value = map_page.get_search_field_value()
        print(f"[DATA] Ожидалось: {city} | В поле по факту: {entered_value}")
        assert entered_value == city
        print("[SUCCESS] Поиск по городу успешно валидирован.")


@allure.feature("Pickup Points Map")
@allure.story("Search By Criteria")
@allure.title("Verify interactive map search by ZIP postal code")
@allure.severity(allure.severity_level.NORMAL)
def test_search_by_zip_code(driver):
    print("\n[START] test_search_by_zip_code")
    zip_code = "11000"
    map_page = MapPage(driver)

    with allure.step("Open pickup points map"):
        map_page.open()

    with allure.step("Handle all cookie banners"):
        map_page.accept_cookies()

    with allure.step(f"Enter ZIP Code: {zip_code}"):
        map_page.enter_search_query(zip_code)
        print(f"[INFO] Индекс '{zip_code}' отправлен в поле поиска.")

    with allure.step("Verify entered ZIP code input value"):
        entered_value = map_page.get_search_field_value()
        print(f"[DATA] Ожидалось: {zip_code} | В поле по факту: {entered_value}")
        assert entered_value == zip_code
        print("[SUCCESS] Поиск по ZIP-коду успешно валидирован.")