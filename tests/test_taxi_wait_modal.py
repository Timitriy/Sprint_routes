import re
import pytest

from data.test_data import PRESET_ADDRESSES
from pages.taxi_flow_page import TaxiFlowPage
from locators.taxi_flow_locators import TaxiFlowLocators as L


@pytest.mark.taxi_order
class TestTaxiWaitModal:
    """
    Полный happy-flow заказа тарифа «Рабочий»:
      • окно «Поиск машины»;
      • финальное окно «Заказ создан»;
      • панель «Детали» + проверка цены, адресов, способа оплаты.
    """

    def test_wait_and_done_details(self, order_page):
        flow = TaxiFlowPage(order_page.driver)
        flow.click(L.WORK_TARIFF_CARD) # тариф рабочий

        # 1) запоминаем стоимость в активной карточке тарифа
        price_before = flow.active_tariff_price()          

        # 2) оформляем заказ: Рабочий + столик ➜ «Ввести номер и заказать»
        flow.prepare_and_submit()

        # 3) модалка «Поиск машины»
        flow.wait_for_wait_modal()
        assert flow.modal_title() == "Поиск машины"
        assert re.fullmatch(r"\d{2}:\d{2}", flow.timer_value())
        assert flow.buttons_present()

        # 4) ждём, пока поиск закончится (заголовок сменится на «N мин. …»)
        flow.wait_until_done(timeout=45)
        assert re.match(r"\d+\s+мин\.", flow.done_title())

        # 5) открываем панель «Детали»
        flow.open_done_details()
        lines = flow.details_main_lines()

        # 5-a: адреса совпадают с введёнными
        assert PRESET_ADDRESSES[0] in lines[0], "Адрес подачи не совпадает"
        assert PRESET_ADDRESSES[1] in lines[1], "Адрес назначения не совпадает"

        # 5-b: способ оплаты указан «Наличные»
        assert any("Наличные" in line for line in lines), "Способ оплаты неверный"

        # 5-c: стоимость совпадает (сравниваем только число рублей)
        price_before_num  = re.search(r"\d+", price_before).group()
        price_after_num   = re.search(r"\d+", flow.details_cost_text()).group()
        assert price_before_num == price_after_num, "Стоимость изменилась"

        flow.click_cancel()

        if not flow.modal_is_closed():
            pytest.xfail("BUG-103: кнопка «Отменить» не закрывает окно")

        
