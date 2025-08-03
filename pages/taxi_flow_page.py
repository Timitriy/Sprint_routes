import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from .base_page import BasePage
from locators.taxi_flow_locators import TaxiFlowLocators as L
class TaxiFlowPage(BasePage):
    """Шаги для сценария: Рабочий + столик → модалка «Поиск машины»."""

    # ────────── вспомогательные шаги ──────────────────────────────────────
    def expand_requirements(self):
        self.click(L.REQS_ARROW)
        self.wait_until_visible(L.LAPTOP_ROW)

    def enable_laptop_switch(self):
        row     = self.wait_until_visible(L.LAPTOP_ROW)
        slider  = row.find_element(*L.LAPTOP_SLIDER)
        inp_box = row.find_element(*L.LAPTOP_INPUT)

        if not inp_box.is_selected():
            ActionChains(self.driver).move_to_element(slider).click().perform()
            self.wait.until(lambda _: inp_box.is_selected())

    # ────────── оформить заказ ────────────────────────────────────────────
    def prepare_and_submit(self):
        """Выбрать тариф «Рабочий», включить столик и нажать «Ввести номер…»."""
        self.click(L.WORK_TARIFF_CARD)
        self.expand_requirements()
        self.enable_laptop_switch()
        self.click(L.ORDER_BTN)

    # ────────── модалка «Поиск машины» ────────────────────────────────────
    def wait_for_wait_modal(self):
        self.wait_until_visible(L.WAIT_MODAL)

    def modal_title(self) -> str:
        return self.text_of(L.WAIT_TITLE)

    def timer_value(self) -> str:
        return self.text_of(L.WAIT_TIMER)

    def buttons_present(self) -> bool:
        return all(self.find(loc).is_displayed() for loc in (
            L.WAIT_CANCEL_BTN, L.WAIT_DETAIL_BTN))

    # ────────── ожидание смены статуса на «Заказ создан» ──────────────────
    def wait_until_done(self, timeout: int = 45):
        """Ждём, пока заголовок сменится с «Поиск машины» на «N мин. и приедет ›»."""
        pattern = re.compile(r"\d+\s+мин\.")
        self.wait_until(
            lambda d: pattern.match(self.text_of(L.DONE_TITLE)),
            timeout=timeout
        )

    def done_title(self) -> str:
        return self.text_of(L.DONE_TITLE)

    def open_done_details(self):
        self.click(L.DONE_DETAIL_BTN)
        self.wait_until_visible(L.DETAILS_PANEL)

    def details_main_lines(self) -> list[str]:
        """Возвращает список жирных строк панели «Детали» (адрес подачи, назначения, способ оплаты, стоимость)."""
        return [el.text.strip() for el in self.finds(L.DETAILS_ROWS_HD)]

    # ────────── данные о стоимости ────────────────────────────────────────
    def active_tariff_price(self) -> str:
        """Цена, отображаемая на карточке активного тарифа (до оформления)."""
        return self.text_of(L.ACTIVE_PRICE)

    def details_cost_text(self) -> str:
        """Строка «Стоимость – N ₽» в панели «Детали»."""
        return self.text_of(L.DETAILS_COST)

    # ────────── кнопка «Отменить» ─────────────────────────────────────────
    def click_cancel(self):
        """Нажимаем кнопку «Отменить» в итоговой модалке."""
        self.click(L.WAIT_CANCEL_BTN)

    def modal_is_closed(self) -> bool:
        """True, если итоговая модалка исчезла с экрана."""
        try:
            return not self.find(L.DONE_MODAL).is_displayed()
        except NoSuchElementException:
            return True

    # ────────── выбрать тариф «Рабочий» (доп. метод) ──────────────────────
    def choose_work_tariff(self):
        """Кликаем по карточке «Рабочий» и ждём, пока она станет активной."""
        self.click(L.WORK_TARIFF_CARD)