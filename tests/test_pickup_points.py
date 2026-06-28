import allure
from pages.map_page import MapPage
from test_data import SEARCH_CITY, SEARCH_ZIP_CODE


@allure.feature("Pickup Points Map")
@allure.story("Map Page Navigation")
@allure.title("Verify pickup points map page opens successfully")
@allure.severity(allure.severity_level.CRITICAL)
def test_pickup_points_page(driver):
    map_page = MapPage(driver)

    with allure.step("Open pickup points map URL"):
        map_page.open()

    with allure.step("Handle all cookie banners"):
        map_page.accept_cookies()

    with allure.step("Verify current landing URL"):
        current_url = map_page.get_current_url()
        assert "mapa-vydejnich-mist" in current_url, (
            f"Expected URL to contain 'mapa-vydejnich-mist', "
            f"but actual URL is '{current_url}'."
        )


@allure.feature("Pickup Points Map")
@allure.story("Search Field Verification")
@allure.title("Verify map search input field is displayed")
@allure.severity(allure.severity_level.NORMAL)
def test_search_field_displayed(driver):
    map_page = MapPage(driver)

    with allure.step("Open pickup points map"):
        map_page.open()

    with allure.step("Handle all cookie banners"):
        map_page.accept_cookies()

    with allure.step("Locate map search field input"):
        search_field = map_page.get_search_field()

    with allure.step("Verify search field is present"):
        assert search_field is not None, (
            "Map search field not found on the page."
        )


@allure.feature("Pickup Points Map")
@allure.story("Search By Criteria")
@allure.title("Verify interactive map search by city name")
@allure.severity(allure.severity_level.NORMAL)
def test_search_by_city(driver):
    map_page = MapPage(driver)

    with allure.step("Open pickup points map"):
        map_page.open()

    with allure.step("Handle all cookie banners"):
        map_page.accept_cookies()

    with allure.step(f"Enter city name: {SEARCH_CITY}"):
        map_page.enter_search_query(SEARCH_CITY)

    with allure.step("Verify entered city input value"):
        entered_value = map_page.get_search_field_value()
        assert entered_value == SEARCH_CITY, (
            f"Expected search field to contain '{SEARCH_CITY}', "
            f"but got '{entered_value}'."
        )


@allure.feature("Pickup Points Map")
@allure.story("Search By Criteria")
@allure.title("Verify interactive map search by ZIP postal code")
@allure.severity(allure.severity_level.NORMAL)
def test_search_by_zip_code(driver):
    map_page = MapPage(driver)

    with allure.step("Open pickup points map"):
        map_page.open()

    with allure.step("Handle all cookie banners"):
        map_page.accept_cookies()

    with allure.step(f"Enter ZIP code: {SEARCH_ZIP_CODE}"):
        map_page.enter_search_query(SEARCH_ZIP_CODE)

    with allure.step("Verify entered ZIP code input value"):
        entered_value = map_page.get_search_field_value()
        assert entered_value == SEARCH_ZIP_CODE, (
            f"Expected search field to contain '{SEARCH_ZIP_CODE}', "
            f"but got '{entered_value}'."
        )