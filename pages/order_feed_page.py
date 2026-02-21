import allure
from selenium.common.exceptions import TimeoutException
from locators.order_feed_locators import OrderFeedLocators
from pages.base_page import BasePage
from logger import logger


class OrderFeedPage(BasePage):

    @allure.step("Получить количество выполненных заказов за всё время")
    def get_total_orders_count(self):
        return int(self.get_text(OrderFeedLocators.TOTAL_ORDERS))

    @allure.step("Получить количество выполненных заказов за сегодня")
    def get_today_orders_count(self):
        return int(self.get_text(OrderFeedLocators.TODAY_ORDERS))

    @allure.step("Получить номер заказа в работе")
    def get_order_number_in_progress(self):
        return self.get_text(OrderFeedLocators.ORDER_NUMBER_IN_PROGRESS)

    @allure.step("Проверить наличие номера заказа в разделе 'В работе'")
    def is_order_in_progress(self, order_number):
        locator = (
            OrderFeedLocators.ORDER_NUMBER_IN_PROGRESS[0],
            f"{OrderFeedLocators.ORDER_NUMBER_IN_PROGRESS[1]}[contains(text(), '{order_number}')]"
        )
        try:
            self.wait_for_element_visible(locator)
            return True
        except TimeoutException:
            return False
