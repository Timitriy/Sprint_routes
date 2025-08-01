import pytest
from pages.main_page import MainPage
from data.test_data import PRESET_ADDRESSES

@pytest.mark.route_block
class TestRouteBlock:

    def test_block_is_shown_for_two_different_addresses(self, driver):
        main = MainPage(driver)
        main.fill_route(*PRESET_ADDRESSES)
        assert main.is_route_block_visible()

    def test_block_text_for_same_address(self, driver):
        addr = PRESET_ADDRESSES[0]
        main = MainPage(driver)
        main.fill_route(addr, addr)

        assert main.is_route_block_visible()
        assert main.route_result_text() == "Авто Бесплатно"
        assert main.route_result_time() == "0 мин."
