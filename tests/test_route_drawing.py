import pytest
from pages.main_page import MainPage
from data.test_data import PRESET_ADDRESSES
@pytest.mark.route_drawing
class TestRouteDrawing:

    def test_two_points_are_drawn(self, driver):
        """
        При вводе двух разных предустановленных адресов
        на карте должны отобразиться точки A и B.
        """
        main = MainPage(driver)
        main.fill_route(*PRESET_ADDRESSES)   # ["Хамовнический вал, 34", "Зубовский бульвар, 37"]
        assert main.are_two_markers_displayed()

