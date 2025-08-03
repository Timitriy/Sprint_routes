import pytest
from data.test_data import TARIFF_DESCRIPTIONS  
@pytest.mark.prepare_taxi
class TestPrepareTaxiOrder:
    """
    Проверка блока результатов маршрута и доступности действий
    перед оформлением заказа такси.

    """
    @pytest.mark.xfail(reason="BUG-201: после смены режима не пересчитываются стоимость/время")
    def test_mode_switch_recalculates_time_and_cost(self, route_block_page):
        page = route_block_page

        # «Оптимальный» выставлен по умолчанию
        cost_opt = page.result_cost()
        time_opt = page.result_time()

        # Переключаемся на «Быстрый»
        page.select_mode("Быстрый")
        assert page.active_mode() == "Быстрый"

        cost_fast = page.result_cost()
        time_fast = page.result_time()

        # Стоимость и/или время должны измениться
        assert (cost_fast, time_fast) != (cost_opt, time_opt)

    def test_custom_mode_enables_all_types(self, route_block_page):
        page = route_block_page

        page.select_mode("Свой")
        assert page.active_mode() == "Свой"

        # Проверяем, что каждый тип становится активным по клику
        for name in ("Машина", "Пешком", "Такси", "Велосипед", "Самокат", "Драйв"):
            page.select_type(name)
            assert page.is_type_active(page.TYPE_CSS[name])

    def test_call_taxi_button_enabled_in_fast_mode(self, route_block_page):
        page = route_block_page

        page.select_mode("Быстрый")
        assert page.is_call_taxi_enabled()

    def test_book_drive_button_enabled_in_custom_drive(self, route_block_page):
        page = route_block_page

        page.select_mode("Свой")
        page.select_type("Драйв")
        assert page.is_book_drive_enabled()
