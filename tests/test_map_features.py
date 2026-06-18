import allure
import time
from pages.map_page import MapPage


@allure.feature("Map Features")
@allure.story("Filters and Geolocation")
@allure.title("Verify geolocation and map filters")
def test_map_features(driver):
    map_page = MapPage(driver)

    with allure.step("Open pickup points map"):
        map_page.open()
        # Доп. ожидание готовности виджета
        time.sleep(5)

    with allure.step("Accept cookies"):
        map_page.accept_cookies()

    with allure.step("Verify and click geolocation button"):
        map_page.click_geolocation_button()
        # Даем карте время на реакцию
        time.sleep(3)

    with allure.step("Open filters panel"):
        map_page.open_filters_panel()

    with allure.step("Apply filters"):
        map_page.apply_filters()