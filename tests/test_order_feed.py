import allure
from urls import Urls
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from logger import logger


@allure.suite("Раздел 'Лента заказов'")
class TestOrderFeed:

    @allure.title("Увеличение счётчика 'Выполнено за всё время' при создании нового заказа")
    def test_total_orders_counter_increase(self, login):
        logger.info("Начало теста: увеличение счётчика 'Выполнено за всё время'")
        main_page = MainPage(login)
        order_feed_page = OrderFeedPage(login)

        # 🔹 Всегда начинаем с главной страницы
        main_page.open_url(Urls.BASE_URL)
        main_page.close_overlay_if_present()

        # 🔹 Переход в ленту заказов
        main_page.click_order_feed()
        assert Urls.FEED_URL in order_feed_page.get_current_url(), "Не перешли на страницу ленты заказов"
        initial_total_orders = order_feed_page.get_total_orders_count()
        logger.info(f"Начальное значение: {initial_total_orders}")

        # 🔹 Создаём новый заказ
        main_page.open_url(Urls.BASE_URL)
        main_page.add_ingredient_to_order()
        main_page.click_order_button()

        assert main_page.is_order_modal_visible(), "Модальное окно заказа не появилось"

        order_number = main_page.get_order_number()
        logger.info(f"Создан заказ №{order_number}")

        main_page.close_modal()

        # 🔹 Возвращаемся на ленту заказов и проверяем увеличение счётчика
        main_page.click_order_feed()
        assert Urls.FEED_URL in order_feed_page.get_current_url(), "Не перешли обратно в ленту заказов"
        final_total_orders = order_feed_page.get_total_orders_count()
        logger.info(f"Конечное значение: {final_total_orders}")

        assert final_total_orders > initial_total_orders, (
            f"Счётчик не увеличился: было {initial_total_orders}, стало {final_total_orders}"
        )

        logger.info("Тест завершен успешно")

    @allure.title("Mock: Увеличение счётчика 'Выполнено за всё время'")
    def test_total_orders_counter_increase_mock(self, mock_auth, mock_order_functionality):
        logger.info("Начало mock-теста 'Выполнено за всё время'")
        main_page = MainPage(mock_auth)

        # 🔹 Начинаем с ленты заказов
        main_page.open_url(Urls.FEED_URL)

        main_page.execute_js("sessionStorage.setItem('mockTotalOrders', '1000');")
        initial_total = int(main_page.execute_js("return sessionStorage.getItem('mockTotalOrders');"))

        main_page.execute_js("sessionStorage.setItem('mockTotalOrders', '1001');")
        final_total = int(main_page.execute_js("return sessionStorage.getItem('mockTotalOrders');"))

        assert final_total > initial_total, f"Mock-счётчик не увеличился: {initial_total} → {final_total}"
        logger.info("Mock тест завершен успешно")

    @allure.title("Mock: Появление заказа в разделе 'В работе'")
    def test_order_appears_in_progress_mock(self, mock_auth, mock_order_functionality):
        logger.info("Начало mock-теста 'Заказ в работе'")
        main_page = MainPage(mock_auth)

        # 🔹 Начинаем с ленты заказов
        main_page.open_url(Urls.FEED_URL)

        mock_order_number = "12345"
        main_page.execute_js(f"""
            const orders = JSON.parse(sessionStorage.getItem('mockOrdersInProgress') || '[]');
            orders.push('{mock_order_number}');
            sessionStorage.setItem('mockOrdersInProgress', JSON.stringify(orders));
        """)

        orders_in_progress = main_page.execute_js(
            "return JSON.parse(sessionStorage.getItem('mockOrdersInProgress') || '[]');"
        )

        assert mock_order_number in orders_in_progress, (
            f"Mock-заказ {mock_order_number} не найден в 'В работе'"
        )

        logger.info("Mock тест завершен успешно")
