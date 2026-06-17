import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    options = Options()

    # Определение того, где мы работаем
    is_ci = os.getenv("CI") == "true"

    if is_ci:
        options.add_argument("--headless=new")  # Более современный headless-режим
    else:
        options.add_argument("--headless")  # или уберите --headless совсем для локальной отладки

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Геолокация
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.geolocation": 1})

    # Инициализация драйвера
    # В GitHub Actions браузер уже установлен, поэтому можно не использовать менеджер,
    # либо использовать его с осторожностью.
    if is_ci:
        driver = webdriver.Chrome(options=options)
    else:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    # Разрешение геолокации
    try:
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