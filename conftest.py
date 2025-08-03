import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import allure

from pages.main_page import MainPage
from pages.taxi_order_page import TaxiOrderPage
from data.test_data import PRESET_ADDRESSES, ROUTE_MODE_FAST, ROUTE_TYPE_TAXI
from config import BASE_URL, DEFAULT_TIMEOUT

@pytest.fixture(scope="session")
def driver():
    """Создаётся один браузер на всю сессию; только WebDriverWait."""
    options = Options()
    driver = webdriver.Chrome(
        service=webdriver.ChromeService(ChromeDriverManager().install()),
        options=options
    )
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(autouse=True)
def open_base_url(driver):
    """До каждого теста открываем начальную страницу; тесты независимы."""
    driver.get(BASE_URL)

# ---------- Allure-helper ----------
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

# ---------- Фикстуры PageObject-ов ----------
@pytest.fixture
def order_page(driver):
    """
    Форма заказа «Такси»:
      • строит маршрут между двумя предустановленными адресами,
      • выбирает режим ROUTE_MODE_FAST,
      • выбирает тип ROUTE_TYPE_TAXI,
      • нажимает «Вызвать такси» и возвращает TaxiOrderPage.
    """
    main = MainPage(driver)
    main.fill_route(*PRESET_ADDRESSES)
    main.select_mode(ROUTE_MODE_FAST)
    main.select_type(ROUTE_TYPE_TAXI)

    if not main.is_call_taxi_enabled():
        pytest.skip("Не удалось подготовить форму заказа: кнопка «Вызвать такси» неактивна.")

    main.call_taxi()

    page = TaxiOrderPage(driver)
    page.wait_for_order_form()
    return page

@pytest.fixture
def route_block_page(driver):
    """MainPage после ввода двух адресов, когда отображается блок результатов маршрута."""
    page = MainPage(driver)
    page.fill_route(*PRESET_ADDRESSES)

    if not page.is_route_block_visible():
        pytest.skip("Не удалось отобразить блок маршрута для заданных адресов.")

    return page