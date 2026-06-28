import allure
from pages.homepage_page import HomepagePage


@allure.feature("Meta Tags")
@allure.story("Page Title")
@allure.title("Verify page title")
def test_page_title(driver):
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        page.open()

    with allure.step("Verify page title text"):
        title = page.get_title()
        assert title != "", (
            "Page title is empty."
        )
        assert "PPL" in title, (
            f"Expected 'PPL' in page title, but got '{title}'."
        )


@allure.feature("Meta Tags")
@allure.story("Meta Description")
@allure.title("Verify meta description")
def test_meta_description(driver):
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        page.open()

    with allure.step("Verify meta description content"):
        description = page.get_meta_description()
        assert description != "", (
            "Meta description is empty."
        )
        assert "PPL" in description, (
            f"Expected 'PPL' in meta description, but got '{description}'."
        )


@allure.feature("Meta Tags")
@allure.story("Open Graph")
@allure.title("Verify Open Graph title")
def test_og_title(driver):
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        page.open()

    with allure.step("Verify og:title content"):
        title = page.get_og_title()
        assert title != "", (
            "og:title tag is empty."
        )
        assert "PPL" in title, (
            f"Expected 'PPL' in og:title, but got '{title}'."
        )


@allure.feature("Meta Tags")
@allure.story("Open Graph")
@allure.title("Verify Open Graph description")
def test_og_description(driver):
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        page.open()

    with allure.step("Verify og:description content"):
        description = page.get_og_description()
        assert description != "", (
            "og:description tag is empty."
        )
        assert "PPL" in description, (
            f"Expected 'PPL' in og:description, but got '{description}'."
        )


@allure.feature("Meta Tags")
@allure.story("Open Graph")
@allure.title("Verify Open Graph URL")
def test_og_url(driver):
    page = HomepagePage(driver)

    with allure.step("Open homepage"):
        page.open()

    with allure.step("Verify og:url content"):
        url = page.get_og_url()
        assert url != "", (
            "og:url tag is empty."
        )
        assert url.startswith("https://"), (
            f"Expected og:url to start with 'https://', but got '{url}'."
        )
        assert "ppl.cz" in url, (
            f"Expected 'ppl.cz' in og:url, but got '{url}'."
        )