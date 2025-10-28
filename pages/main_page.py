import allure
from selenium.common.exceptions import TimeoutException
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from logger import logger


class MainPage(BasePage):

    @allure.step("Проверить видимость модального окна ингредиента")
    def is_ingredient_modal_visible(self):
        try:
            self.wait_for_element_visible(MainPageLocators.INGREDIENT_MODAL)
            return True
        except TimeoutException:
            logger.info("Модальное окно ингредиента не видимо")
            return False

    @allure.step("Получить название ингредиента в модальном окне")
    def get_ingredient_modal_name(self):
        return self.get_text(MainPageLocators.INGREDIENT_MODAL_NAME)

    @allure.step("Закрыть модальное окно")
    def close_modal(self):
        self.click(MainPageLocators.CLOSE_MODAL_BUTTON)

    @allure.step("Проверить, что модальное окно закрыто")
    def is_modal_closed(self):
        try:
            self.wait_for_element_invisible(MainPageLocators.INGREDIENT_MODAL)
            return True
        except TimeoutException:
            return False

    @allure.step("Добавить ингредиент в заказ")
    def add_ingredient_to_order(self):
        logger.info("Добавление ингредиента в заказ")
        source = self.find(MainPageLocators.INGREDIENT_CARD)
        target = self.find(MainPageLocators.CONSTRUCTOR_AREA)
        self.driver.execute_script(
            """
            const dataTransfer = new DataTransfer();
            arguments[0].dispatchEvent(new DragEvent('dragstart', { dataTransfer }));
            arguments[1].dispatchEvent(new DragEvent('drop', { dataTransfer }));
            """, source, target
        )

    @allure.step("Получить значение счётчика ингредиента")
    def get_ingredient_counter_value(self):
        try:
            text = self.get_text(MainPageLocators.INGREDIENT_COUNTER)
            return int(text)
        except TimeoutException:
            return 0

    @allure.step("Нажать кнопку оформления заказа")
    def click_order_button(self):
        self.click(MainPageLocators.ORDER_BUTTON)

    @allure.step("Проверить видимость модального окна заказа")
    def is_order_modal_visible(self):
        try:
            self.wait_for_element_visible(MainPageLocators.ORDER_MODAL)
            return True
        except TimeoutException:
            self.take_screenshot("order_modal_not_visible")
            return False

    @allure.step("Получить номер заказа")
    def get_order_number(self):
        return self.get_text(MainPageLocators.ORDER_NUMBER)

    @allure.step("Перейти в личный кабинет")
    def go_to_personal_account(self):
        self.click(MainPageLocators.PERSONAL_ACCOUNT)

    @allure.step("Проверить видимость ингредиентов")
    def is_ingredient_visible(self):
        return self.is_element_present(MainPageLocators.INGREDIENT_CARD)

    @allure.step("Получить название ингредиента")
    def get_ingredient_name(self):
        return self.get_text(MainPageLocators.INGREDIENT_NAME)

    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self):
        self.click(MainPageLocators.INGREDIENT_CARD)

    @allure.step("Кликнуть на ленту заказов")
    def click_order_feed(self):
        self.click(MainPageLocators.ORDER_FEED_BUTTON)

    @allure.step("Кликнуть на конструктор")
    def click_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_BUTTON)

    @allure.step("Закрыть оверлей, если он присутствует")
    def close_overlay_if_present(self):
        from selenium.common.exceptions import TimeoutException
        from locators.main_page_locators import MainPageLocators
        try:
            self.wait_for_element_visible(MainPageLocators.OVERLAY)
            self.click(MainPageLocators.OVERLAY)
            logger.info("Оверлей был закрыт")
        except TimeoutException:
            logger.debug("Оверлей отсутствует — ничего не закрываем")

