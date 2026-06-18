import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    options = Options()
    is_ci = os.getenv("CI") == "true" or os.getenv("HEADLESS") == "true"

    if is_ci:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        # КРИТИЧНО ДЛЯ КАРТ В CI: отключаем запросы разрешений
        options.add_argument("--use-fake-ui-for-media-stream")
        options.add_argument("--disable-geolocation")
        options.add_argument("--disable-notifications")

    options.add_argument("--window-size=1920,1080")

    # Автоматическое разрешение геолокации
    prefs = {
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()