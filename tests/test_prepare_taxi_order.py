import pytest
from pages.main_page import MainPage
from data.test_data import PRESET_ADDRESSES

@pytest.mark.prepare_taxi
class TestPrepareTaxiOrder:

    def _open_route_block(self, driver):
        page = MainPage(driver)
        page.fill_route(*PRESET_ADDRESSES)
        assert page.is_route_block_visible()
        return page

    # 1. Смена между «Оптимальный» ↔ «Быстрый»
    @pytest.mark.xfail(reason="BUG-201: не пересчитываются стоимость/время при переключении режима")
    def test_mode_switch_recalculates_time_and_cost(self, driver):
        page = self._open_route_block(driver)

        cost_opt  = page.result_cost()
        time_opt  = page.result_time() 

        page.select_mode("Быстрый")
        assert page.active_mode() == "Быстрый"

        cost_fast = page.result_cost()
        time_fast = page.result_time()

        # баг: значения совпадают
        assert (cost_fast, time_fast) != (cost_opt, time_opt)

    # 2. «Свой» включает все типы передвижения
    def test_custom_mode_enables_all_types(self, driver):
        page = self._open_route_block(driver)
        page.select_mode("Свой")
        assert page.active_mode() == "Свой"

        for t in ("Машина", "Пешком", "Такси", "Велосипед", "Самокат", "Драйв"):
            page.select_type(t)
            assert page.is_type_active(page.TYPE_CSS[t])


    # 3. В «Быстрый» кнопка «Вызвать такси» доступна
    def test_call_taxi_button_enabled_in_fast_mode(self, driver):
        page = self._open_route_block(driver)
        page.select_mode("Быстрый")
        assert page.is_call_taxi_enabled()

    # 4. В «Свой» + «Драйв» доступна кнопка «Забронировать»
    def test_book_drive_button_enabled_in_custom_drive(self, driver):
        page = self._open_route_block(driver)
        page.select_mode("Свой")
        page.select_type("Драйв")
        assert page.is_book_drive_enabled()
