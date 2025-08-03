from selenium.webdriver.common.action_chains import ActionChains
from .base_page import BasePage
from locators.taxi_order_locators import TaxiOrderLocators as L
from selenium.webdriver.support import expected_conditions as EC


class TaxiOrderPage(BasePage):
    """PageObject формы заказа «Такси»."""

    # ─── появление формы ───────────────────────────────────────────────────────
    def wait_for_order_form(self):
        self.wait_until_visible(L.TARIFF_CARD_TITLES)

    # ─── тарифы ────────────────────────────────────────────────────────────────
    def tariff_titles(self) -> list[str]:
        return [el.text.strip()
                for el in self.driver.find_elements(*L.TARIFF_CARD_TITLES)]

    def active_tariff(self) -> str:
        return (self.driver.find_element(*L.TARIFF_CARD_ACTIVE)
                           .find_element(*L.TARIFF_CARD_TITLES)
                           .text.strip())

    def select_tariff(self, name: str):
        self.click(L.TARIFF_CARD_BY_TITLE(name))

    # ---------- работа с тултипом ----------
    def hover_info(self, name: str):
        btn = self.wait_until_visible(L.INFO_BTN_BY_TITLE(name))
        ActionChains(self.driver).move_to_element(btn).pause(0.2).perform()
        self.wait.until(
            lambda d: any(el.is_displayed() 
                          for el in d.find_elements(*L.TOOLTIP_DESC))
        )

    def tooltip_description(self) -> str:
        for el in self.driver.find_elements(*L.TOOLTIP_DESC):
            if el.is_displayed():
                return el.text.strip()
        return ""

    def close_tooltip(self):
        """Увести курсор на карту, чтобы закрыть всплывающее окно."""
        ActionChains(self.driver).move_by_offset(400, 0).perform()
        self.wait.until(
            lambda d: all(not el.is_displayed()
                          for el in d.find_elements(*L.TOOLTIP_DESC))
        )

    # наличие базовых полей под тарифами
    def basic_fields_present(self) -> bool:
        """Проверяем, отображаются ли все четыре обязательных поля под блоком тарифов: Телефон, Способ оплаты, Комментарий, Требования к заказу."""
        from locators.taxi_order_locators import TaxiOrderLocators as L
        return all(
            self.driver.find_element(*loc).is_displayed()
            for loc in (L.PHONE_FIELD, L.PAYMENT_FIELD,
                        L.COMMENT_INPUT, L.REQS_HEADER)
        )