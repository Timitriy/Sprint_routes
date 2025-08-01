from .base_locators import By


class MainPageLocators:
    """Локаторы стартового экрана."""

    # --- поля ввода адресов ---
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")

    # --- карта ---
    # «A» и «B» — буквенные ярлыки маленьких пинов построенного маршрута
    MAP_PIN_A = (By.CSS_SELECTOR, 'ymaps[class*="route-pin__label-0"]')
    MAP_PIN_B = (By.CSS_SELECTOR, 'ymaps[class*="route-pin__label-1"]')

    # ---------- блок выбора маршрута ----------
    ROUTE_BLOCK         = (By.CSS_SELECTOR, "div.type-picker.shown")
    ROUTE_RESULT_TEXT   = (By.CSS_SELECTOR, "div.type-picker.shown div.results-text .text")
    ROUTE_RESULT_TIME   = (By.CSS_SELECTOR, "div.type-picker.shown div.results-text .duration")

    # ---------- вкладки «Оптимальный / Быстрый / Свой» ----------
    MODE_TAB = lambda text: (By.XPATH, f'//div[@class="modes-container"]/div[normalize-space()="{text}"]')
    MODE_TAB_ACTIVE = (By.CSS_SELECTOR, 'div.modes-container .mode.active')

    # ---------- типы передвижения внутри режима «Свой» ----------
    TYPE_ICON = lambda css_part: (By.CSS_SELECTOR, f'div.types-container .type{css_part}')

    # ---------- кнопки ----------
    CALL_TAXI_BTN   = (By.XPATH, '//button[normalize-space()="Вызвать такси"]')
    BOOK_DRIVE_BTN  = (By.XPATH, '//button[normalize-space()="Забронировать"]')
    TYPE_ACTIVE = (By.CSS_SELECTOR, 'div.types-container .type.active')

    