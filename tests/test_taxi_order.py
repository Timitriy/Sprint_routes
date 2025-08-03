import pytest
from data.test_data import TARIFF_DESCRIPTIONS
@pytest.mark.taxi_order
class TestTaxiOrder:
    """Проверки формы заказа тарифа «Такси» (режим «Быстрый»)."""

    # 1. На форме есть шесть тарифов и один из них активен
    def test_tariffs_set_and_active(self, order_page):
        assert set(order_page.tariff_titles()) == set(TARIFF_DESCRIPTIONS)
        assert order_page.active_tariff() in TARIFF_DESCRIPTIONS

    # 2. Все тултипы содержат правильное описание
    @pytest.mark.parametrize(
        "tariff, expected",
        [
            ("Рабочий",      TARIFF_DESCRIPTIONS["Рабочий"]),
            pytest.param(
                "Сонный",
                TARIFF_DESCRIPTIONS["Сонный"],
                marks=pytest.mark.xfail(reason="BUG-101: неверный текст тултипа «Сонный»")
            ),
            ("Отпускной",    TARIFF_DESCRIPTIONS["Отпускной"]),
            pytest.param(
                "Разговорчивый",
                TARIFF_DESCRIPTIONS["Разговорчивый"],
                marks=pytest.mark.xfail(reason="BUG-102: неверный текст тултипа «Разговорчивый»")
            ),
            ("Утешительный", TARIFF_DESCRIPTIONS["Утешительный"]),
            ("Глянцевый",    TARIFF_DESCRIPTIONS["Глянцевый"]),
        ],
        ids=[
            "Рабочий", "Сонный (bug)", "Отпускной",
            "Разговорчивый (bug)", "Утешительный", "Глянцевый"
        ],
    )

    def test_tooltip_text(self, order_page, tariff, expected):
        """
        Наводим курсор на «i» в карточке тарифа и убеждаемся,
        что текст всплывающего описания соответствует ТЗ.
        """
        order_page.select_tariff(tariff)
        order_page.hover_info(tariff)
        actual = order_page.tooltip_description()

        
        assert actual == expected, f"Неверное описание тарифа «{tariff}»: {actual!r}"
        order_page.close_tooltip()

    # 3. Под каждым тарифом отображается набор обязательных полей
    def test_basic_fields_present_under_each_tariff(self, order_page):
        for tariff in TARIFF_DESCRIPTIONS:
            order_page.select_tariff(tariff)
            assert order_page.basic_fields_present(), \
                f"Блок полей не отрисован для тарифа «{tariff}»"
