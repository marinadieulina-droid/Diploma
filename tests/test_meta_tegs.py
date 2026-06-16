import allure

from selenium.webdriver.common.by import By


@allure.feature("Meta Tags")
@allure.story("Page Title")
@allure.title("Verify page title")
def test_page_title(driver):

    driver.get("https://www.ppl.cz")

    title = driver.title

    print(f"\nPage Title: {title}")

    assert title != ""
    assert "PPL" in title


@allure.feature("Meta Tags")
@allure.story("Meta Description")
@allure.title("Verify meta description")
def test_meta_description(driver):

    driver.get("https://www.ppl.cz")

    meta_description = driver.find_element(
        By.XPATH,
        "//meta[@name='description']"
    )

    description = meta_description.get_attribute(
        "content"
    )

    print(f"\nMeta Description: {description}")

    assert description != ""


@allure.feature("Meta Tags")
@allure.story("Open Graph")
@allure.title("Verify Open Graph title")
def test_og_title(driver):

    driver.get("https://www.ppl.cz")

    og_title = driver.find_element(
        By.XPATH,
        "//meta[@property='og:title']"
    )

    title = og_title.get_attribute(
        "content"
    )

    print(f"\nOG Title: {title}")

    assert title != ""


@allure.feature("Meta Tags")
@allure.story("Open Graph")
@allure.title("Verify Open Graph description")
def test_og_description(driver):

    driver.get("https://www.ppl.cz")

    og_description = driver.find_element(
        By.XPATH,
        "//meta[@property='og:description']"
    )

    description = og_description.get_attribute(
        "content"
    )

    print(f"\nOG Description: {description}")

    assert description != ""


@allure.feature("Meta Tags")
@allure.story("Open Graph")
@allure.title("Verify Open Graph URL")
def test_og_url(driver):

    driver.get("https://www.ppl.cz")

    og_url = driver.find_element(
        By.XPATH,
        "//meta[@property='og:url']"
    )

    url = og_url.get_attribute(
        "content"
    )

    print(f"\nOG URL: {url}")

    assert url != ""
