import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():

    options = webdriver.ChromeOptions()

    # Разрешаем геолокацию
    options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.geolocation": 1
        }
    )

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    )

    # Разрешение геолокации для ppl.cz
    driver.execute_cdp_cmd(
        "Browser.grantPermissions",
        {
            "origin": "https://www.ppl.cz",
            "permissions": ["geolocation"]
        }
    )

    # Подставляем координаты Праги
    driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {
            "latitude": 50.0755,
            "longitude": 14.4378,
            "accuracy": 100
        }
    )

    driver.maximize_window()

    yield driver

    driver.quit()