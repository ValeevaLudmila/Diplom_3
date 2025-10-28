from selenium.webdriver.common.by import By


class OrderFeedLocators:
    # ===== СЧЁТЧИКИ ЗАКАЗОВ =====
    TOTAL_ORDERS = (By.XPATH, "//p[contains(text(), 'Выполнено за все время')]/following-sibling::p")
    TODAY_ORDERS = (By.XPATH, "//p[contains(text(), 'Выполнено за сегодня')]/following-sibling::p")

    # ===== ЗАКАЗЫ В РАБОТЕ =====
    IN_PROGRESS_SECTION = (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderList')]")
    ORDER_NUMBER_IN_PROGRESS = (By.XPATH, "//li[contains(@class, 'OrderFeed_order__number')]")
