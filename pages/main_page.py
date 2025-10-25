import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from logger import logger


class MainPage(BasePage):

    @allure.step("Проверить видимость модального окна ингредиента")
    def is_ingredient_modal_visible(self):
        logger.debug("Проверка видимости модального окна ингредиента")
        try:
            self.wait_for_element(MainPageLocators.INGREDIENT_MODAL, timeout=20)
        except TimeoutException:
            logger.info("Модальное окно ингредиента не видимо")
            return False
        else:
            logger.info("Модальное окно ингредиента видимо")
            return True
    
    @allure.step("Получить название ингредиента в модальном окне")
    def get_ingredient_modal_name(self):
        logger.debug("Получение названия ингредиента в модальном окне")
        name = self.get_text_on_element(MainPageLocators.INGREDIENT_MODAL_NAME)
        logger.info("Название в модальном окне: %s", name)
        return name

    @allure.step("Закрыть модальное окно")
    def close_modal(self):
        logger.info("Закрытие модального окна")
        self.click_on_element(MainPageLocators.CLOSE_MODAL_BUTTON)

    @allure.step("Проверить, что модальное окно закрыто")
    def is_modal_closed(self):
        """Проверить, что модальное окно закрыто."""
        logger.debug("Проверка закрытия модального окна")
        try:
            self.wait_for_element_hide(MainPageLocators.INGREDIENT_MODAL, timeout=5)
        except TimeoutException:
            logger.info("Модальное окно не закрыто")
            return False
        else:
            logger.info("Модальное окно закрыто")
            return True

    @allure.step("Добавить ингредиент в заказ")
    def add_ingredient_to_order(self):
        logger.info("Добавление ингредиента в заказ")
        self.drag_and_drop_element(
            MainPageLocators.INGREDIENT_CARD, MainPageLocators.CONSTRUCTOR_AREA
        )

    @allure.step("Получить значение счетчика ингредиента")
    def get_ingredient_counter_value(self):
        """Получить значение счетчика ингредиента."""
        logger.debug("Получение значения счетчика ингредиента")
        try:
            counter_element = self.wait_for_element(
                MainPageLocators.INGREDIENT_COUNTER, timeout=3
            )
        except TimeoutException:
            logger.info("Счетчик ингредиента не найден, значение: 0")
            return 0
        else:
            value = int(counter_element.text)
            logger.info("Значение счетчика ингредиента: %s", value)
            return value

    @allure.step("Нажать кнопку оформления заказа")
    def click_order_button(self):
        logger.info("Нажатие кнопки оформления заказа")
        self.safe_click_with_overlay(MainPageLocators.ORDER_BUTTON)

    @allure.step("Проверить видимость модального окна заказа")
    def is_order_modal_visible(self):
        """Проверить видимость модального окна заказа."""
        logger.debug("Проверка видимости модального окна заказа")
        self.wait_for_overlay_to_disappear(timeout=10)
        try:
            self.wait_for_element(MainPageLocators.ORDER_MODAL, timeout=40)
            logger.info("Модальное окно заказа видимо")
            return True
        except TimeoutException:
            logger.warning("Модальное окно заказа не появилось за 40 секунд")
            self.take_screenshot("order_modal_not_visible")
            allure.attach.file(
                f"logs/order_modal_not_visible.png",
                name="order_modal_not_visible",
                attachment_type=allure.attachment_type.PNG
            )
            return False



    @allure.step("Получить номер заказа")
    def get_order_number(self):
        logger.debug("Получение номера заказа")
        number = self.get_text_on_element(MainPageLocators.ORDER_NUMBER)
        logger.info("Номер заказа: %s", number)
        return number
    
    @allure.step("Перейти в личный кабинет")
    def go_to_personal_account(self):
        """Перейти в личный кабинет."""
        logger.info("Переход в личный кабинет")
        self.safe_click_with_overlay(MainPageLocators.PERSONAL_ACCOUNT)

    @allure.step("Ожидать загрузки страницы")
    def wait_for_page_load(self, timeout=10):
        """Ожидать полной загрузки страницы."""
        logger.debug("Ожидание загрузки страницы")
        self.wait_for_condition(
            lambda driver: driver.execute_script("return document.readyState") == "complete",
            timeout=timeout,
            description="полная загрузка страницы"
        )

    @allure.step("Проверить видимость ингредиентов")
    def is_ingredient_visible(self):
        """Проверить, видны ли ингредиенты на странице."""
        logger.debug("Проверка видимости ингредиентов")
        try:
            return self.is_element_present(MainPageLocators.INGREDIENT_CARD, timeout=5)
        except Exception as e:
            logger.error("Ошибка при проверке ингредиентов: %s", e)
            return False
        
    @allure.step("Получить название ингредиента")
    def get_ingredient_name(self):
        logger.debug("Получение названия ингредиента")
        name = self.get_text_on_element(MainPageLocators.INGREDIENT_NAME)
        logger.info("Название ингредиента: %s", name)
        return name
    
    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self):
        logger.info("Клик на ингредиент")
        self.click_on_element(MainPageLocators.INGREDIENT_CARD)

    @allure.step("Кликнуть на ленту заказов")
    def click_order_feed(self):
        logger.info("Клик на ленту заказов")
        self.safe_click_with_overlay(MainPageLocators.ORDER_FEED_BUTTON)

    @allure.step("Кликнуть на конструктор")
    def click_constructor(self):
        logger.info("Клик на конструктор")
        self.safe_click_with_overlay(MainPageLocators.CONSTRUCTOR_BUTTON)