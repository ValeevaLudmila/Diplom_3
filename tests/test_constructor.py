import allure
import pytest
from urls import Urls
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

        # 🔹 Главная страница
        main_page.open_url(Urls.BASE_URL)
        main_page.close_overlay_if_present()

        main_page.click_order_feed()
        assert Urls.FEED_URL in order_feed_page.get_current_url(), "Не перешли на ленту заказов"

        main_page.click_constructor()
        assert Urls.BASE_URL in main_page.get_current_url(), "Не вернулись в конструктор"

        logger.info("Тест завершен: переход по конструктору работает корректно")

    @allure.title("Переход по клику на раздел 'Лента заказов'")
    def test_click_order_feed(self, login):
        logger.info("Начало теста: Переход по клику на 'Лента заказов'")
        main_page = MainPage(login)
        order_feed_page = OrderFeedPage(login)

        main_page.open_url(Urls.BASE_URL)
        main_page.close_overlay_if_present()

        main_page.click_order_feed()
        assert Urls.FEED_URL in order_feed_page.get_current_url(), "Не перешли на ленту заказов"

        logger.info("Тест завершен: переход на ленту заказов работает корректно")

    @allure.title("Открытие модального окна с деталями ингредиента")
    def test_ingredient_modal_opening(self, login):
        logger.info("Начало теста: Открытие модального окна ингредиента")
        main_page = MainPage(login)

        main_page.open_url(Urls.BASE_URL)

        ingredient_name = main_page.get_ingredient_name()
        logger.info(f"Название ингредиента: {ingredient_name}")

        main_page.click_ingredient()
        assert main_page.is_ingredient_modal_visible(), "Модальное окно не открылось"

        modal_ingredient_name = main_page.get_ingredient_modal_name()
        assert ingredient_name == modal_ingredient_name, "Название ингредиента в модалке не совпадает"

        logger.info("Тест завершен успешно")

    @allure.title("Закрытие модального окна по клику на крестик")
    def test_ingredient_modal_closing(self, login):
        logger.info("Начало теста: Закрытие модального окна ингредиента")
        main_page = MainPage(login)

        main_page.open_url(Urls.BASE_URL)
        main_page.close_overlay_if_present()

        main_page.click_ingredient()
        assert main_page.is_ingredient_modal_visible(), "Модалка не открылась"

        main_page.close_modal()
        assert main_page.is_modal_closed(), "Модалка не закрылась"

        logger.info("Тест завершен: модальное окно закрывается корректно")

    @allure.title("Увеличение счетчика ингредиента при добавлении в заказ")
    def test_ingredient_counter_increase(self, login):
        logger.info("Начало теста: Увеличение счетчика ингредиента")
        main_page = MainPage(login)

        main_page.open_url(Urls.BASE_URL)
        main_page.close_overlay_if_present()

        initial_counter = main_page.get_ingredient_counter_value()
        logger.info(f"Начальное значение счетчика: {initial_counter}")

        main_page.add_ingredient_to_order()

        final_counter = main_page.get_ingredient_counter_value()
        logger.info(f"Конечное значение счетчика: {final_counter}")

        expected_increase = 2
        actual_increase = final_counter - initial_counter

        assert actual_increase == expected_increase, (
            f"Счетчик увеличился на {actual_increase}, ожидалось: {expected_increase}. "
            f"Было: {initial_counter}, стало: {final_counter}"
        )

        logger.info("Тест завершен: счетчик ингредиента увеличивается корректно")
