import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    options = Options()

    # Проверяем обе переменные: CI (стандарт GitHub) и HEADLESS (наша)
    is_ci = os.getenv("CI") == "true" or os.getenv("HEADLESS") == "true"

    if is_ci:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 1})

    # Инициализация драйвера
    if is_ci:
        driver = webdriver.Chrome(options=options)
    else:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    # Установка геолокации
    try:
        driver.get("https://www.ppl.cz")
        driver.execute_cdp_cmd("Browser.grantPermissions", {
            "origin": "https://www.ppl.cz",
            "permissions": ["geolocation"]
        })
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
            "latitude": 50.0755,
            "longitude": 14.4378,
            "accuracy": 100
        })
    except Exception as e:
        print(f"\n[WARNING] Не удалось установить геолокацию: {e}")

    yield driver
    driver.quit()