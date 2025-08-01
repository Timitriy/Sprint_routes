import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import allure

from pages.main_page import MainPage
from pages.taxi_order_page import TaxiOrderPage
from data.test_data import PRESET_ADDRESSES
from config import BASE_URL, DEFAULT_TIMEOUT


@pytest.fixture(scope="session")
def driver():
    """Создаётся один браузер на всю сессию; no‑implicit‑waits, только WebDriverWait."""
    options = Options()
    driver = webdriver.Chrome(
        service=webdriver.ChromeService(ChromeDriverManager().install()),
        options=options
    )
    driver.maximize_window() 
    #driver.set_window_size(1440, 900)
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def open_base_url(driver):
    """До каждого теста открываем начальную страницу; тесты независимы."""
    driver.get(BASE_URL)


# ---------- Allure‑helper ----------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """При падении теста делаем скрин и логи в Allure."""
    outcome = yield
    rep = outcome.get_result()
    if rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )

@pytest.fixture
def order_page(driver):
    """
    Готовит форму заказа «Такси» (предусловия для всех тестов):
      1) строит маршрут «Быстрый» между двумя предустановленными адресами,
      2) выбирает тип маршрута «Такси»,
      3) открывает форму заказа и возвращает объект TaxiOrderPage.
    """
    main = MainPage(driver)
    main.fill_route(*PRESET_ADDRESSES)
    main.select_mode("Быстрый")
    main.select_type("Такси")
    assert main.is_call_taxi_enabled()  #
    main.call_taxi()

    page = TaxiOrderPage(driver)
    page.wait_for_order_form()
    return page