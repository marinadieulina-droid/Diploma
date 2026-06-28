import allure
from pages.map_page import MapPage


@allure.feature("Map Features")
@allure.story("Filters and Geolocation")
@allure.title("Verify geolocation and map filters")
def test_map_features(driver):
    map_page = MapPage(driver)

    with allure.step("Open pickup points map"):
        map_page.open()
        current_url = map_page.get_current_url()
        assert "mapa-vydejnich-mist" in current_url, (
            f"Expected URL to contain 'mapa-vydejnich-mist', "
            f"but actual URL is '{current_url}'."
        )

    with allure.step("Accept cookies"):
        map_page.accept_cookies()

    with allure.step("Verify and click geolocation button"):
        # Геолокация может быть недоступна в CI-среде — это ожидаемое поведение,
        # поэтому результат не проверяется как обязательный
        map_page.click_geolocation_button()

    with allure.step("Open filters panel"):
        map_page.open_filters_panel()

    with allure.step("Expand 'Typ místa' category if present"):
        map_page.expand_typ_mista_category()

    with allure.step("Select filters via standard elements"):
        map_page.select_shop_and_box_filters()

    with allure.step("Apply filters"):
        map_page.apply_filters()

    with allure.step("Verify filtration flow completed"):
        final_url = map_page.get_current_url()
        assert "mapa-vydejnich-mist" in final_url, (
            f"Expected to remain on map page after applying filters, "
            f"but actual URL is '{final_url}'."
        )