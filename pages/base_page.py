from typing import Callable
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from config import DEFAULT_TIMEOUT
class BasePage:

    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # ─── low-level find ───────────────────────────────────────────────────
    def find(self, locator):
        return self.driver.find_element(*locator)

    def finds(self, locator):
        return self.driver.find_elements(*locator)

    # ─── helpers ──────────────────────────────────────────────────────────
    def text_of(self, locator) -> str:
        return self.find(locator).text.strip()

    def attr_of(self, locator, attr: str):
        return self.find(locator).get_attribute(attr)

    # ─── explicit waits ───────────────────────────────────────────────────
    def wait_until_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_until_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def wait_until(self, predicate: Callable, timeout: int | None = None):
        return WebDriverWait(self.driver, timeout or DEFAULT_TIMEOUT).until(predicate)

    # ─── elementary actions ───────────────────────────────────────────────
    def click(self, locator):
        self.wait_until_clickable(locator).click()

    def input(self, locator, text: str):
        el = self.wait_until_visible(locator)
        el.clear()
        el.send_keys(text)

    def scroll_into_view(self, locator):
        el = self.wait_until_visible(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", el
        )
        return el

    def scroll_and_click(self, locator):
        el = self.scroll_into_view(locator)
        self.wait_until_clickable(locator)
        try:
            el.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", el)