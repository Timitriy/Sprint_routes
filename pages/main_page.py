from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from locators.main_page_locators import MainPageLocators as L
from locators.base_locators import By

class MainPage(BasePage):

    # ─── вспомогательные ──────────────────────────────────────────────────
    def _fill_input(self, locator, text: str):
        """Ввод текста + ENTER и ожидание скрытия выпадающего списка подсказок."""
        self.input(locator, text + Keys.ENTER)
        self.wait_until_invisible(L.SUGGEST_LIST)

    # ─── публичные шаги ───────────────────────────────────────────────────
    def fill_route(self, from_addr: str, to_addr: str):
        self._fill_input(L.FROM_FIELD, from_addr)
        self._fill_input(L.TO_FIELD,   to_addr)

    # ─── проверки карты ───────────────────────────────────────────────────
    def are_two_markers_displayed(self) -> bool:
        self.wait_until_visible(L.MAP_PIN_A)
        self.wait_until_visible(L.MAP_PIN_B)
        return self.find(L.MAP_PIN_A).is_displayed() and self.find(L.MAP_PIN_B).is_displayed()

    # ─── блок результатов ─────────────────────────────────────────────────
    def is_route_block_visible(self) -> bool:
        return self.wait_until_visible(L.ROUTE_BLOCK).is_displayed()

    def route_result_text(self) -> str:
        return self.text_of(L.ROUTE_RESULT_TEXT)

    def route_result_time(self) -> str:
        raw = self.text_of(L.ROUTE_RESULT_TIME)
        return raw.replace("В пути", "").strip()

    # ─── работа с режимами ────────────────────────────────────────────────
    def select_mode(self, name: str):
        self.click(L.MODE_TAB(name))
        self.wait_until_visible(L.MODE_TAB_ACTIVE)

    def active_mode(self) -> str:
        return self.text_of(L.MODE_TAB_ACTIVE)

    # ─── работа с типами (режим «Свой») ───────────────────────────────────
    TYPE_CSS = {
        "Машина":    "",
        "Пешком":    "",
        "Такси":     "",
        "Велосипед": "",
        "Самокат":   "",
        "Драйв":     ".drive",
    }

    def select_type(self, name: str):
        self.click(L.TYPE_ICON(self.TYPE_CSS[name]))
        self.wait_until_visible(L.TYPE_ACTIVE)

    def active_type(self) -> str:
        return self.attr_of(L.TYPE_ACTIVE, "innerText").strip()

    # ─── стоимость / время ────────────────────────────────────────────────
    def result_cost(self) -> str:
        return self.route_result_text()

    def result_time(self) -> str:
        return self.route_result_time()

    # ─── доступность кнопок ───────────────────────────────────────────────
    def is_call_taxi_enabled(self) -> bool:
        return self.wait_until_visible(L.CALL_TAXI_BTN).is_enabled()

    def is_book_drive_enabled(self) -> bool:
        return self.wait_until_visible(L.BOOK_DRIVE_BTN).is_enabled()

    # ─── иконка типа активна? ──────────────────────────────────────────────
    def is_type_active(self, css_suffix: str = "") -> bool:
        locator = (By.CSS_SELECTOR, f'div.types-container .type.active{css_suffix}')
        try:
            return self.find(locator).is_displayed()
        except Exception:
            return False

    # ─── вызвать такси ────────────────────────────────────────────────────
    def call_taxi(self):
        self.click(L.CALL_TAXI_BTN)
        self.wait_until_invisible(L.CALL_TAXI_BTN)
