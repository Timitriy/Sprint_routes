from .base_locators import By

class MainPageLocators:
    """Локаторы стартового экрана."""

    # ─── поля ввода адресов ────────────────────────────────────────────────
    FROM_FIELD = (By.ID, "from")
    TO_FIELD   = (By.ID, "to")

    # ─── карта ─────────────────────────────────────────────────────────────
    MAP_PIN_A = (By.CSS_SELECTOR, 'ymaps[class*="route-pin__label-0"]')
    MAP_PIN_B = (By.CSS_SELECTOR, 'ymaps[class*="route-pin__label-1"]')

    # ─── блок результатов маршрута ────────────────────────────────────────
    ROUTE_BLOCK       = (By.CSS_SELECTOR, "div.type-picker.shown")
    ROUTE_RESULT_TEXT = (By.CSS_SELECTOR, "div.type-picker.shown div.results-text .text")
    ROUTE_RESULT_TIME = (By.CSS_SELECTOR, "div.type-picker.shown div.results-text .duration")

    # ─── вкладки «Оптимальный / Быстрый / Свой» ───────────────────────────
    MODE_TAB        = lambda txt: (By.XPATH, f'//div[@class="modes-container"]/div[normalize-space()="{txt}"]')
    MODE_TAB_ACTIVE = (By.CSS_SELECTOR, 'div.modes-container .mode.active')

    # ─── типы передвижения (режим «Свой») ─────────────────────────────────
    TYPE_ICON  = lambda css: (By.CSS_SELECTOR, f'div.types-container .type{css}')
    TYPE_ACTIVE = (By.CSS_SELECTOR, 'div.types-container .type.active')

    # ─── кнопки действия ──────────────────────────────────────────────────
    CALL_TAXI_BTN  = (By.XPATH, '//button[normalize-space()="Вызвать такси"]')
    BOOK_DRIVE_BTN = (By.XPATH, '//button[normalize-space()="Забронировать"]')

    # ─── выпадающий список автодополнения ─────────────────────────────────
    SUGGEST_LIST = (By.CSS_SELECTOR, ".suggest__list")
