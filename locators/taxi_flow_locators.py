from .base_locators import By


class TaxiFlowLocators:
    """Локаторы для сценария заказа тарифа «Рабочий»."""

    # --- форма заказа -------------------------------------------------------
    WORK_TARIFF_CARD = (
        By.XPATH,
        '//div[@class="tcard-title" and text()="Рабочий"]/ancestor::div[contains(@class,"tcard")]'
    )
    REQS_ARROW = (By.CSS_SELECTOR, "div.reqs-arrow")

    LAPTOP_ROW    = (
        By.XPATH,
        '//div[@class="r-sw-container" and .//div[@class="r-sw-label" and '
        'normalize-space()="Столик для ноутбука"]]'
    )
    LAPTOP_SLIDER = (By.CSS_SELECTOR, "span.slider.round")
    LAPTOP_INPUT  = (By.CSS_SELECTOR, "input.switch-input")

    ORDER_BTN = (
        By.XPATH,
        '//button[contains(@class,"smart-button") and '
        './/span[contains(text(),"Ввести номер и заказать")]]'
    )

    # --- модалка «Поиск машины» --------------------------------------------
    WAIT_MODAL      = (By.CSS_SELECTOR, "div.order-body")
    WAIT_TITLE      = (By.CSS_SELECTOR, "div.order-header-title")
    WAIT_TIMER      = (By.CSS_SELECTOR, "div.order-header-time")
    WAIT_CANCEL_BTN = (By.XPATH, '//div[@class="order-btn-group"][div="Отменить"]//button')
    WAIT_DETAIL_BTN = (By.XPATH, '//div[@class="order-btn-group"][div="Детали"]//button')

        # --- модалка «Заказ создан» --------------------------------------------
    DONE_MODAL      = (By.CSS_SELECTOR,  "div.order-body")   # у неё тот же корень
    DONE_TITLE      = (By.CSS_SELECTOR,  "div.order-header-title")
    DONE_DETAIL_BTN = (By.XPATH, '//div[@class="order-btn-group"][div="Детали"]//button')

    # --- строки внутри панели «Детали» (открывается тем же DONE_DETAIL_BTN) -
    DETAILS_PANEL   = (By.CSS_SELECTOR, "div.order-details")
    DETAILS_ROWS_HD = (By.CSS_SELECTOR, "div.order-details-content > div.o-d-h")

    # --- цена в активной карточке тарифа (до заказа) -----------------------
    ACTIVE_PRICE = (By.CSS_SELECTOR, "div.tcard.active div.tcard-price")

    # --- строка «Стоимость – …» в панели «Детали» ---------------------------
    DETAILS_COST = (
        By.XPATH,
        '//div[@class="order-details-row"][.//div[@class="o-d-h" and text()="Еще про поездку"]]'
        '//div[contains(@class,"o-d-sh")]'
    )