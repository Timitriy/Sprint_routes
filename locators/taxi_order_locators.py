from .base_locators import By


class TaxiOrderLocators:
    """Локаторы формы заказа тарифа «Такси»."""

    # корень формы
    ORDER_FORM = (By.CSS_SELECTOR, "div.order-modal")

    # ─── тарифы ─────────────────────────────────────────────────────────────────
    TARIFF_CARD_TITLES = (By.CSS_SELECTOR, "div.tcard-title")          # все названия
    TARIFF_CARD_ACTIVE = (By.CSS_SELECTOR, "div.tcard.active")         # активная
    TARIFF_CARD_BY_TITLE = (
        lambda name: (By.XPATH,
                      f'//div[@class="tcard-title" and normalize-space()="{name}"]/..')
    )

    # «i»-кнопка и тултип
    INFO_BTN_BY_TITLE = (
    lambda name: (By.XPATH,
        f'//div[@class="tcard-title" and normalize-space()="{name}"]'
        f'/ancestor::div[contains(@class,"tcard")]'
        f'//button[contains(@class,"tcard-i")]')
        )
    TOOLTIP_DESC = (By.CSS_SELECTOR, ".i-floating .i-dPrefix")

    # ─── блок полей под тарифами ───────────────────────────────────────────────
    PHONE_FIELD   = (By.CSS_SELECTOR, "div.np-button .np-text")
    PAYMENT_FIELD = (By.CSS_SELECTOR, "div.pp-button .pp-text")
    COMMENT_INPUT = (By.CSS_SELECTOR, 'input#comment')
    REQS_HEADER   = (By.CSS_SELECTOR, "div.reqs-header .reqs-head")
    
