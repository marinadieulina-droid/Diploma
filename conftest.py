import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    options = Options()

    # Настройки для сервера (GitHub Actions)
    options.add_argument("--headless")  # Запуск без графического интерфейса
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Ваши настройки геолокации
    options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.geolocation": 1
        }
    )

    # Инициализация драйвера
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Разрешение геолокации и установка координат Праги
    driver.execute_cdp_cmd(
        "Browser.grantPermissions",
        {
            "origin": "https://www.ppl.cz",
            "permissions": ["geolocation"]
        }
    )
    driver.execute_cdp_cmd(
        "Emulation.setGeolocationOverride",
        {
            "latitude": 50.0755,
            "longitude": 14.4378,
            "accuracy": 100
        }
    )

    yield driver
    driver.quit()