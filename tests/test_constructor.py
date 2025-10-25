import allure
import pytest
from data import Urls
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from logger import logger


@allure.suite("Проверка основной функциональности")
class TestMainFunctionality:
    
    @allure.title("Переход по клику на 'Конструктор'")
    def test_click_constructor(self, login):
        logger.info("Начало теста: Переход по клику на 'Конструктор'")
        main_page = MainPage(login)
        order_feed_page = OrderFeedPage(login)
        
        logger.debug("Обработка возможного OVERLAY перед тестом")
        main_page.close_overlay_if_present()
        
        logger.debug("Переход на ленту заказов")
        main_page.click_order_feed()
        assert Urls.FEED_URL in order_feed_page.get_current_url()
        
        logger.debug("Возврат в конструктор")
        main_page.click_constructor()
        assert Urls.BASE_URL in main_page.get_current_url()
        logger.info("Тест завершен: переход по конструктору работает корректно")

    @allure.title("Переход по клику на раздел 'Лента заказов'")
    def test_click_order_feed(self, login):
        logger.info("Начало теста: Переход по клику на 'Лента заказов'")
        main_page = MainPage(login)
        order_feed_page = OrderFeedPage(login)
        
        logger.debug("Обработка возможного OVERLAY перед тестом")
        main_page.close_overlay_if_present()
        
        logger.debug("Клик на ленту заказов")
        main_page.click_order_feed()
        assert Urls.FEED_URL in order_feed_page.get_current_url()
        logger.info("Тест завершен: переход на ленту заказов работает корректно")

    @allure.title("Открытие модального окна с деталями ингредиента")
    def test_ingredient_modal_opening(self, login):
        logger.info("Начало теста: Открытие модального окна ингредиента")
        main_page = MainPage(login)
    
        from data import Urls
        current_url = main_page.get_current_url()
        if "login" in current_url:
            logger.info("Переходим с страницы логина на главную...")
            main_page.driver.get(Urls.BASE_URL)
            main_page.wait_for_page_load()
    
        try:
            # Пробуем получить название ингредиента
            ingredient_name = main_page.get_ingredient_name()
            logger.info("Название ингредиента: %s", ingredient_name)
        
            logger.debug("Клик на ингредиент")
            main_page.click_ingredient()
        
            assert main_page.is_ingredient_modal_visible()
        
            # Получаем название из модального окна
            modal_ingredient_name = main_page.get_ingredient_modal_name()
            assert ingredient_name == modal_ingredient_name
        
            logger.info("Тест завершен успешно")
        
        except Exception as e:
            logger.error("Ошибка в тесте: %s", e)
            main_page.take_screenshot("test_error")
            pytest.fail(f"Тест упал с ошибкой: {e}")

    @allure.title("Закрытие модального окна по клику на крестик")
    def test_ingredient_modal_closing(self, login):
        logger.info("Начало теста: Закрытие модального окна ингредиента")
        main_page = MainPage(login)
        
        logger.debug("Обработка возможного OVERLAY перед тестом")
        main_page.close_overlay_if_present()
        
        logger.debug("Открытие модального окна")
        main_page.click_ingredient()
        assert main_page.is_ingredient_modal_visible()
        
        logger.debug("Закрытие модального окна")
        main_page.close_modal()
        
        logger.debug("Проверка закрытия модального окна")
        assert main_page.is_modal_closed()
        logger.info("Тест завершен: модальное окно закрывается корректно")

    @allure.title("Увеличение счетчика ингредиента при добавлении в заказ")
    def test_ingredient_counter_increase(self, login):
        logger.info("Начало теста: Увеличение счетчика ингредиента")
        main_page = MainPage(login)
        
        logger.debug("Обработка возможного OVERLAY перед тестом")
        main_page.close_overlay_if_present()
        
        logger.debug("Получение начального значения счетчика")
        initial_counter = main_page.get_ingredient_counter_value()
        logger.info("Начальное значение счетчика: %s", initial_counter)
        
        logger.debug("Добавление ингредиента в заказ")
        main_page.add_ingredient_to_order()
        
        logger.debug("Получение конечного значения счетчика")
        final_counter = main_page.get_ingredient_counter_value()
        logger.info("Конечное значение счетчика: %s", final_counter)
        
        expected_increase = 2
        actual_increase = final_counter - initial_counter
    
        assert actual_increase == expected_increase, (
            f"Счетчик увеличился на {actual_increase}, ожидалось: {expected_increase}. "
            f"Было: {initial_counter}, стало: {final_counter}"
        )
    
        logger.info("Тест завершен: счетчик ингредиента увеличивается корректно")