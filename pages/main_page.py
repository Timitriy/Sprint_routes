from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage
from locators.main_page_locators import MainPageLocators as L
from locators.base_locators import By


class MainPage(BasePage):

    # ---------- вспомогательные ----------
    def _fill_input(self, locator, text: str):
        self.input(locator, text + Keys.ENTER)
        self.wait.until(EC.invisibility_of_element_located(
            ('css selector', '.suggest__list')
        ))

    # ---------- публичные шаги ----------
    def fill_route(self, from_addr: str, to_addr: str):
        self._fill_input(L.FROM_FIELD, from_addr)
        self._fill_input(L.TO_FIELD,   to_addr)

    # ---------- проверки карты ----------
    def are_two_markers_displayed(self) -> bool:
        self.wait_until_visible(L.MAP_PIN_A)
        self.wait_until_visible(L.MAP_PIN_B)
        return (
            self.driver.find_element(*L.MAP_PIN_A).is_displayed() and
            self.driver.find_element(*L.MAP_PIN_B).is_displayed()
        )

    # ---------- проверки блока маршрута ----------
    def is_route_block_visible(self) -> bool:
        return self.wait_until_visible(L.ROUTE_BLOCK).is_displayed()

    def route_result_text(self) -> str:
        return self.driver.find_element(*L.ROUTE_RESULT_TEXT).text.strip()

    def route_result_time(self) -> str:
        raw = self.driver.find_element(*L.ROUTE_RESULT_TIME).text.strip()
        return raw.replace("В пути", "").strip()
    
    # ---------- работа с режимами ----------
    def select_mode(self, name: str):
        """Кликаем по вкладке 'Оптимальный' | 'Быстрый' | 'Свой'."""
        self.click(L.MODE_TAB(name))
        self.wait_until_visible(L.MODE_TAB_ACTIVE)
    
    def active_mode(self) -> str:
        """Возвращает текст активной вкладки."""
        return self.driver.find_element(*L.MODE_TAB_ACTIVE).text.strip()

    # ---------- работа с типами передвижения (только для «Свой») ----------
    TYPE_CSS = {
        "Машина":     "",           # ".type"
        "Пешком":     "",           # ".type"
        "Такси":      "",           # ".type"
        "Велосипед":  "",           # ".type"
        "Самокат":    "",           # ".type"
        "Драйв":      ".drive",     # ".type.drive"
    }

    def select_type(self, name: str):
        css_part = self.TYPE_CSS[name]
        self.click(L.TYPE_ICON(css_part))
        self.wait_until_visible(L.TYPE_ACTIVE)

    def active_type(self) -> str:
        return self.driver.find_element(*L.TYPE_ACTIVE).get_attribute("innerText").strip()  

    # ---------- стоимость и время ----------
    def result_cost(self) -> str:
        return self.route_result_text()

    def result_time(self) -> str:
        return self.route_result_time()

    # ---------- доступность кнопок ----------
    def is_call_taxi_enabled(self) -> bool:
        btn = self.wait_until_visible(L.CALL_TAXI_BTN)
        return btn.is_enabled()

    def is_book_drive_enabled(self) -> bool:
        btn = self.wait_until_visible(L.BOOK_DRIVE_BTN)
        return btn.is_enabled()
    
    # ---------- проверка, что иконка типа активна ---------
    def is_type_active(self, css_suffix: str = "") -> bool:
        """True, если в контейнере есть .type.active[.drive]"""
        locator = (By.CSS_SELECTOR,
                   f'div.types-container .type.active{css_suffix}')
        try:
            return self.driver.find_element(*locator).is_displayed()
        except Exception:
            return False
        
    # ---------- доступность кнопок ----------
    def is_call_taxi_enabled(self) -> bool:
        btn = self.wait_until_visible(L.CALL_TAXI_BTN)       
        return btn.is_enabled()

    # ---------- новый шаг ----------
    def call_taxi(self):
        """Кликаем «Вызвать такси» и ждём, пока кнопка исчезнет."""
        self.click(L.CALL_TAXI_BTN)
        self.wait.until(EC.invisibility_of_element_located(L.CALL_TAXI_BTN))