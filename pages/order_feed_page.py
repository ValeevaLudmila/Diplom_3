import allure
from selenium.common.exceptions import TimeoutException
from locators.order_feed_locators import OrderFeedLocators
from pages.base_page import BasePage
from logger import logger


class OrderFeedPage(BasePage):
    
    @allure.step("Получить количество выполненных заказов за все время")
    def get_total_orders_count(self):
        logger.debug("Получение количества заказов за все время")
        count = int(self.get_text_on_element(OrderFeedLocators.TOTAL_ORDERS))
        logger.info("Выполнено за все время: %s", count)
        return count

    @allure.step("Получить количество выполненных заказов за сегодня")
    def get_today_orders_count(self):
        logger.debug("Получение количества заказов за сегодня")
        count = int(self.get_text_on_element(OrderFeedLocators.TODAY_ORDERS))
        logger.info("Выполнено за сегодня: %s", count)
        return count

    @allure.step("Получить номер заказа в работе")
    def get_order_number_in_progress(self):
        logger.debug("Получение номера заказа в работе")
        number = self.get_text_on_element(OrderFeedLocators.ORDER_NUMBER_IN_PROGRESS)
        logger.info("Номер заказа в работе: %s", number)
        return number

    @allure.step("Проверить наличие номера заказа в разделе 'В работе'")
    def is_order_in_progress(self, order_number):
        """Проверить наличие номера заказа в разделе 'В работе'."""
        logger.debug("Проверка наличия заказа %s в разделе 'В работе'", order_number)
        order_locator = (
            OrderFeedLocators.ORDER_NUMBER_IN_PROGRESS[0], 
            f"{OrderFeedLocators.ORDER_NUMBER_IN_PROGRESS[1]}[contains(text(), '{order_number}')]"
        )
        
        try:
            is_present = self.wait_for_element(order_locator, timeout=5)
        except TimeoutException:
            logger.info("Заказ %s в разделе 'В работе': False", order_number)
            return False
        else:
            logger.info("Заказ %s в разделе 'В работе': True", order_number)
            return is_present