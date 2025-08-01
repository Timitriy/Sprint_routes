import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage
from locators.taxi_flow_locators import TaxiFlowLocators as L


class TaxiFlowPage(BasePage):
    """Шаги для сценария: Рабочий + столик → окно «Поиск машины»."""

    # ------------ вспомогательные шаги -------------------------------------
    def expand_requirements(self):
        self.click(L.REQS_ARROW)
        self.wait_until_visible(L.LAPTOP_ROW)

    def enable_laptop_switch(self):
        row = self.wait_until_visible(L.LAPTOP_ROW)
        slider = row.find_element(*L.LAPTOP_SLIDER)
        inp    = row.find_element(*L.LAPTOP_INPUT)

        if not inp.is_selected():
            ActionChains(self.driver).move_to_element(slider).click().perform()
            self.wait.until(lambda _: inp.is_selected())

    # ------------ оформить заказ -------------------------------------------
    def prepare_and_submit(self):
        """Выбрать тариф «Рабочий», включить столик и нажать «Ввести номер…»."""
        self.click(L.WORK_TARIFF_CARD)
        self.expand_requirements()
        self.enable_laptop_switch()
        self.click(L.ORDER_BTN)

    # ------------ модалка «Поиск машины» -----------------------------------
    def wait_for_wait_modal(self):
        self.wait_until_visible(L.WAIT_MODAL)

    def modal_title(self) -> str:
        return self.driver.find_element(*L.WAIT_TITLE).text.strip()

    def timer_value(self) -> str:
        return self.driver.find_element(*L.WAIT_TIMER).text.strip()

    def buttons_present(self) -> bool:
        return all(
            self.driver.find_element(*loc).is_displayed()
            for loc in (L.WAIT_CANCEL_BTN, L.WAIT_DETAIL_BTN)
        )

    # ---------- ожидание модалки «Заказ создан» -----------------------------
    def wait_until_done(self, timeout: int = 45):
        """
        Ждём, когда заголовок сменится с «Поиск машины» на «N мин. и приедет ›».
        """
        WebDriverWait(self.driver, timeout).until(
            lambda d: re.match(r"\d+\s+мин\.", d.find_element(*L.DONE_TITLE).text)
        )

    def done_title(self) -> str:
        return self.driver.find_element(*L.DONE_TITLE).text.strip()

    def open_done_details(self):
        self.click(L.DONE_DETAIL_BTN)
        self.wait_until_visible(L.DETAILS_PANEL)

    def details_main_lines(self) -> list[str]:
        """
        Возвращает список текстов из жирных строк панели «Детали»
        (Адрес подачи, назначения, способ оплаты, стоимость).
        """
        return [el.text.strip() for el in self.driver.find_elements(*L.DETAILS_ROWS_HD)]
    
    # ---------- данные о стоимости -----------------------------------------
    def active_tariff_price(self) -> str:
        """Цена, отображаемая на карточке активного тарифа (до оформления)."""
        return self.driver.find_element(*L.ACTIVE_PRICE).text.strip()

    def details_cost_text(self) -> str:
        """Текст вида «Стоимость – N₽» в панели «Детали»."""
        return self.driver.find_element(*L.DETAILS_COST).text.strip()
    
    # ---------- кнопка «Отменить» ------------------------------------------
    def click_cancel(self):
        """Нажимаем кнопку «Отменить» в итоговой модалке."""
        self.click(L.WAIT_CANCEL_BTN)          # локатор уже существует

    def modal_is_closed(self) -> bool:
        """Возвращает True, если модалка заказа исчезла с экрана."""
        from selenium.common.exceptions import NoSuchElementException

        try:
            return not self.driver.find_element(*L.DONE_MODAL).is_displayed()
        except NoSuchElementException:
            return True
        
    def choose_work_tariff(self):
        """Кликаем по карточке «Рабочий» и ждём, пока она станет активной."""
        self.click(L.WORK_TARIFF_CARD)

